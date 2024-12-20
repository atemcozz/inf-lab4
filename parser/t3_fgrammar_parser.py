import json
from functools import lru_cache
from pprint import pprint
from sys import flags
from types import NoneType
import re

from unicodedata import numeric


class NumberWrapper:
    def __init__(self,  value, form):
        self.value = value
        self.form = form


def __is_float(x):
    try:
        _ = float(x)
    except (TypeError, ValueError):
        return False
    else:
        return True


def __is_int(x):
    try:
        _ = int(x)
    except (TypeError, ValueError):
        return False
    else:
        return True


@lru_cache(None)
def parse_key(string):
    string = string.lstrip()
    cut = string[:string.find('\n')]
    sep_ind = cut.find(":")
    if sep_ind == -1:
        return None
    res = string[:sep_ind].strip()
    return res, string[sep_ind + 1:]


@lru_cache(None)
def parse_number(string):
    string = string.lstrip()
    newline_ind = string.find('\n')
    if newline_ind != -1:
        res = string[:newline_ind].strip()
    else:
        res = string.strip()
    if len(res) == 0 or res.endswith(":"):
        return None

    if __is_int(res):
        res = NumberWrapper(int(res), "normal")
    elif __is_float(res):
        if "e" in res:
            res = NumberWrapper(res, "exp")
        else:
            res = NumberWrapper(float(res), "normal")
    else:
        return None
    remain = string[newline_ind + 1:] if newline_ind != -1 else ''

    return res, remain.strip()


@lru_cache(None)
def parse_null(string):
    nulls = 'null', '~'
    newline_ind = string.find('\n')
    if newline_ind != -1:
        res = string[:newline_ind].strip()
    else:
        res = string.strip()
    if len(res) == 0 or res.endswith(":"):
        return None
    if res.lower() not in nulls:
        return None
    remain = string[newline_ind + 1:] if newline_ind != -1 else ''

    return None, remain.strip()


@lru_cache(None)
def parse_boolean(string):
    _map = {
        True: ('true', 'yes', 'y', 'on'),
        False: ('false', 'no', 'n', 'off')
    }
    newline_ind = string.find('\n')
    if newline_ind != -1:
        res = string[:newline_ind].strip()
    else:
        res = string.strip()
    if len(res) == 0 or res.endswith(":"):
        return None

    if res.lower() in _map[True]:
        res = True
    elif res.lower() in _map[False]:
        res = False
    else:
        return None
    remain = string[newline_ind + 1:] if newline_ind != -1 else ''

    return res, remain.strip()


@lru_cache(None)
def parse_quoted_string(string):
    string = string.lstrip()
    q_sym = string[0]
    i = 1
    while i < len(string):
        if string[i] == '\\':
            i += 2
            continue
        if string[i] == q_sym:
            break
        i += 1
    return string[1:i], string[i+1:]

@lru_cache(None)
def parse_string(string):
    # newline_ind = string.find('\n')
    # if newline_ind != -1:
    #     res = string[:newline_ind].strip()
    # else:
    #     res = string.strip()
    # if len(res) == 0 or res.endswith(":") or ": " in res:
    #     return None
    # remain = string[newline_ind + 1:] if newline_ind != -1 else ''
    # return res.strip(), remain.strip()
    string = string.lstrip()
    if string.startswith("-"):
        return None
        return parse_json_array(string)
    if string.startswith("["):
        return parse_json_array(string)
    if string.startswith('"') or string.startswith("'"):
        return parse_quoted_string(string)
    i = 0
    boundary_found = False
    cur_newlines = 0
    while 0 <= i < len(string):
        if string[i] == '\n':
            cur_newlines += 1
        if string[i:i+2] == ": " or string[i:i+2] == ":\n":
            if cur_newlines == 0:
                return None
            while string[i] != '\n':
                i -= 1
                if i <= 0:
                    i = -1
                    break
            boundary_found = True
        if boundary_found:
            break
        i += 1
    res = string[:i]
    res = re.sub(r"\n\s+", "\n", res)
    if i < 0: return None
    if res.startswith('"') and res.endswith('"'):
        res = res[1:-1]
    return res.strip(), string[i:].strip()

@lru_cache(None)
def parse_key_value(string):
    key = parse_key(string)
    if not key:
        return None
    value = parse_value(key[1])
    if not value:
        return None
    return (key[0], value[0]), value[1]


@lru_cache(None)
def get_object_boundary_pos(string, _from, boundary_indent):
    j = -1
    i = _from
    while i < len(string):
        if string[i] == '\n':
            j = 0
        elif string[i] == ' ' and (string[i - 1] == ' ' or string[i - 1] == '\n'):
            j += 1
        else:
            if j == boundary_indent:
                break
            j = -1
        i += 1
    return i


@lru_cache(None)
def parse_object(string):
    inds_count = 0
    i = 1
    while string[i] == ' ':
        inds_count += 1
        i += 1
    prev_inds = inds_count - 2
    boundary_pos = get_object_boundary_pos(string, i, prev_inds)

    return parse_objects_row(string[:boundary_pos])[0], string[boundary_pos:]

@lru_cache(None)
def parse_json_array(string):
    string = string.lstrip()
    array = []
    if string[0] != "[":
        return None
    i = 1
    j = 1
    while string[i] != "]":
        if string[i] == ",":
            value = parse_value(string[j:i])
            if value:
                array.append(parse_value(string[j:i])[0])
            else: array.append(None)
            j = i + 1
        i += 1
    array.append(parse_value(string[j:i])[0])
    return array, string[i+1:]

@lru_cache(None)
def parse_array(string):

    array = []
    if string[0] != '\n':
        return None
    inds_count = 0
    i = 1
    while string[i] == ' ':
        inds_count += 1
        i += 1
    if string[i:i + 2] != "- ":
        return None
    prev_inds = inds_count - 2
    boundary_pos = get_object_boundary_pos(string, i, prev_inds)
    i += 2
    begin_ptr = i
    # Collecting characters until there is another
    # array element with the same indent or boundary position

    while i <= boundary_pos:
        if string[i:i + inds_count + 2] == '\n' + ' ' * inds_count + "-" or i == boundary_pos:
            parsed = string[begin_ptr:i]
            array.append(parse_value(parsed)[0])
            begin_ptr = i + inds_count + 2
        i += 1
    return array, string[boundary_pos:]


@lru_cache(None)
def parse_objects_row(string):
    res = {}
    while True:
        keyval = parse_key_value(string)
        if not keyval:
            string = ""
            break
        (key, value), rest = keyval
        if key not in res:
            res[key] = value
        string = rest
    return res, string.strip()


@lru_cache(None)
def parse_value(string):

    chain = [parse_null, parse_boolean, parse_number, parse_string, parse_array, parse_object, parse_objects_row]
    res = None
    # Iterating string through subparsers until some part of it is parsed
    for fn in chain:
        if fn(string):
            res = fn(string)
            break
    return (res[0], res[1].strip()) if res else None


def manage_comments(string):
    ctx = []
    lines = string.split('\n')
    print(lines)
    for i in range(len(lines)):
        if re.match(r"(^.*\s*#.*$)|(.*\s+#.*$)", lines[i], flags=re.MULTILINE):
            comment = re.findall(r"#(.*)", lines[i])[0]

            prev_line = lines[i - 1] if i > 0 else ""
            next_line = lines[i + 1] if i < len(lines) - 1 else ""

            res = {
                "comment": comment,
                "line": i,
                "context": '\n'.join([prev_line, lines[i], next_line]),
            }
            ctx.append(res)
    return (re.sub(r"(^.*\s*#.*$)|(\s+#.*$)", "", string, flags=re.MULTILINE), ctx)


@lru_cache(None)
def from_yaml(string):
    string = string.strip()
    string, comments_ctx = manage_comments(string)
    parsed = parse_value(string.strip())

    if parsed is None or parsed[1].strip():
        raise ValueError("Bad string")
    return parsed[0], comments_ctx


def obj_to_json(obj):
    if isinstance(obj, dict):
        keyvalues = []
        for key, value in obj.items():
            ready_value = obj_to_json(value)
            keyvalues.append(f'"{key}": {ready_value}')
        return f'{{ {", ".join(keyvalues)} }}'
    elif isinstance(obj, list):
        ready_values = map(str, [obj_to_json(o) for o in obj])
        return f"[{', '.join(ready_values)}]"
    elif isinstance(obj, NoneType):
        return "null"
    elif isinstance(obj, bool):
        return str(obj).lower()
    elif isinstance(obj, NumberWrapper):
        return str(obj.value)
    elif isinstance(obj, int) or isinstance(obj, float):
        return str(obj)
    elif isinstance(obj, str):
        res = obj[0]
        i = 1
        while i < len(obj):
            if obj[i] == '"' and obj[i-1] != '\\':
                res += '\\"'
                i += 1
                continue
            res += obj[i]
            i += 1
        res = res.replace("\n", "\\n")
        return f'"{res}"'


if __name__ == "__main__":
    file_in2 = open("../resources/etalon.yaml", "r", encoding="UTF-8")
    file_out2 = open("out_etalon.json", "w", encoding="UTF-8")
    comments_out = open("comments.json", "w", encoding="UTF-8")
    content2 = file_in2.read()
    parsed_obj, comments = from_yaml(content2)
    result2 = obj_to_json(parsed_obj)
    print(result2)
    print(comments)
    file_out2.write(result2)
    comments_out.write(obj_to_json(comments))
