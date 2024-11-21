from t3_fgrammar_parser import from_yaml


def obj_to_csv(obj):
    pairs = obj["schedule"]["pairs"]
    rows = []
    header = list(pairs.items())[0][1].keys()
    rows.append(['pair'] + list(header))
    for key, value in pairs.items():
        rows.append([key] + list(value.values()))
    result = '\n'.join(';'.join(f'"{str(item)}"' for item in row) for row in rows)

    return result


if __name__ == "__main__":
    file_in = open("../resources/schedule.yml", "r", encoding="UTF-8")
    file_out = open("out.csv", "w", encoding="cp1251")
    content = file_in.read()
    result = obj_to_csv(from_yaml(content))
    print(result)
    file_out.write(result, )
