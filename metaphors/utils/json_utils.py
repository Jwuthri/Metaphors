import os
import ast
import json

from typing import Dict, Any


def read_json_file(path: str) -> Dict[Any, Any]:
    assert os.path.exists(path), f"file {path} doesn't exists."
    with open(path, "r") as file:
        data = json.load(file)

    return data


def read_text_file(path: str, to_object: bool = False) -> Any:
    assert os.path.exists(path), f"file {path} doesn't exists."
    with open(path, "r") as f:
        data = f.read()

    return data if not to_object else ast.literal_eval(data)
