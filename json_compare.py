import json


def _simple_compare(v1, v2) -> bool:
    return v1 == v2


def _float_compare(v1: float, v2: float) -> bool:
    return abs(round(v1, 5) - round(v2, 5)) < 0.00001


def _compare(obj_one: dict, obj_two: dict) -> dict:
    output = {k: False for k in {k for k in obj_one.keys()} ^ {k for k in obj_two.keys()}}
    for k in {k: False for k in {k for k in obj_one.keys()} & {k for k in obj_two.keys()}}:
        if not isinstance(obj_one[k], type(obj_two[k])):
            output[k] = False
            continue
        if isinstance(obj_one[k], dict):
            output[k] = _compare(obj_one[k], obj_two[k])
            continue
        if isinstance(obj_one[k], float):
            output[k] = _float_compare(obj_one[k], obj_two[k])
            continue
        output[k] = obj_one[k] == obj_two[k]
    return output


def compare(json_str1: str, json_str2: str) -> dict:
    return _compare(json.loads(json_str1), json.loads(json_str2))
