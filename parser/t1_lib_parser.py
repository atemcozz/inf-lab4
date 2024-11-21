import json
import yaml


def yaml_to_json(string):
    return yaml.safe_load(string)


if __name__ == "__main__":
    with open("../resources/etalon.yaml", "r", encoding="UTF-8") as fin,open("lib_etalon.json", "w",
                                                                              encoding="UTF-8") as fout:
        content = fin.read()
        result = yaml_to_json(content)
        json.dump(result, fout, ensure_ascii=False)
