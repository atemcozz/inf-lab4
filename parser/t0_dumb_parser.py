# 9 YAML -> JSON Вторник, пятница(+)


IN_INDENT = ' ' * 2
OUT_INDENT = ' ' * 2


def indent_level(string, indent=IN_INDENT):
    res = 0
    indent_len = len(indent)
    i = 0
    while i < len(string):
        if string[i:i + indent_len] != indent: break
        res += 1
        i += indent_len
    return res


def yaml_to_json(string):
    IN_INDENT = ' ' * 2
    OUT_INDENT = ' ' * 2
    lines = string.split('\n')
    lines = list(filter(lambda el: not el.isspace() and el != '', lines))
    line_index = 0
    while line_index < (len(lines)):
        if lines[line_index].count(":") == 0:
            line_index += 1
            continue
        key, value = lines[line_index].split(':', maxsplit=1)
        ind_level = indent_level(lines[line_index])
        str_indent = OUT_INDENT * ind_level
        # Parse keys for objects
        if not value or value.isspace():
            lines[line_index] = f"{str_indent}\"{key.strip()}\": {{"
            # Check indent levels for each line
            for i in range(line_index + 1, len(lines)):
                if ind_level >= indent_level(lines[i]):
                    lines.insert(i, f"{str_indent}}}")
                    if ind_level == indent_level(lines[i]):
                        lines[i] += ","
                    break
                elif i == len(lines) - 1:
                    lines.append(f"{str_indent}}}")
                    break
        # Parse regular keys
        else:
            lines[line_index] = f"{str_indent}\"{key.strip()}\": \"{value.strip()}\""
            if line_index < len(lines) - 1 and ind_level == indent_level(lines[line_index + 1]):
                lines[line_index] += ","
        line_index += 1
    lines = list(map(lambda x: OUT_INDENT + x, lines))
    lines.insert(0, "{")
    lines.append("}")
    return "\n".join(lines)


if __name__ == "__main__":
    file_in = open("../resources/schedule.yml", "r", encoding="UTF-8")
    file_out = open("out_schedule.json", "w", encoding="UTF-8")
    content = file_in.read()
    result = yaml_to_json(content)
    print(result)
    file_out.write(result)

    file_in.close()
    file_out.close()
