import json


def read_json(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def update_json(path: str, data: dict) -> None:
    with open(path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)