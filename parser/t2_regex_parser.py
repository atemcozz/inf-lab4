import re

# 9 YAML -> JSON Вторник, пятница(+)


# ([\w\-_]+):{1} +([^\n]+) - ключ и значение
# (\s*:\s*{)\n( {6,}[^\n]+\n+)+ - match уровня вложенность (6 пробелов)


def yaml_to_json(string):
    MAX_DEPTH = 8
    # quote keys and values
    string = re.sub(r"([\w\-_]+):{1} +([^\n]+)", fr'"\1": "\2"', string)
    # put opening braces
    string = re.sub(r"([\w\-_]+):{1}(\n|\s+)", fr'"\1": {{\n', string)

    # put closing braces
    for i in range(1, MAX_DEPTH):
        string = re.sub(fr"((\s*:\s*{{)\n( {{{i * 2},}}[^\n]+\n+)+)", fr"\1{' ' * (i - 1) * 2}}}\n", string)

    # Put commas
    string = re.sub(r"\"(\s+)\"", r'",\1"', string)
    string = re.sub(r"}(\s+)\"", r'},\1"', string)

    # fix indents
    string = re.sub(r"^", r"  ", string, flags=re.MULTILINE)
    string = re.sub(r"\s+$", r"", string, flags=re.MULTILINE)

    result = re.sub(r"_", string, "{\n_\n}")
    return result

if __name__ == "__main__":
    file_in = open("../resources/schedule.yml", "r", encoding="UTF-8")
    file_out = open("out.json", "w", encoding="UTF-8")

    content = file_in.read()

    result = yaml_to_json(content)
    print(result)
    file_out.write(result)

    file_in.close()
    file_out.close()
