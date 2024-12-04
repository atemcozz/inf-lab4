
from t3_fgrammar_parser import from_yaml


def obj_to_csv(obj):
    pairs = obj["schedule"]["pairs"]
    rows = []
    header = list(pairs.items())[0][1].keys()
    rows.append(['pair'] + list(header))
    for key, value in pairs.items():
        rows.append([key] + list(value.values()))
    entries = []
    for i in range(len(rows)):
        entries.append([])
        for item in rows[i]:
            if "NumberWrapper" in str(type(item)):
                _str = str(item.value)
            else:
                _str = str(item)
            if ';' in _str:
                _str = _str.replace('"', '""')
                _str = f'"{_str}"'

            entries[i].append(_str)
    result = '\n'.join([';'.join(row) for row in entries])

    return result


if __name__ == "__main__":
    file_in = open("../resources/schedule.yml", "r", encoding="UTF-8")
    file_out = open("out.csv", "w", encoding="cp1251")
    content = file_in.read()
    result = obj_to_csv(from_yaml(content))
    print(result)
    file_out.write(result, )
