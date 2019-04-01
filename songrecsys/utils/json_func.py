import json
from os.path import exists
from typing import Text


def save_to_json(obj: object, where: Text) -> object:
    override = True
    if exists(where):
        answer = input(f'{where} exists. Override? [Yy/Nn] ')
        override = answer in 'YyTt'

    if override:
        with open(where, 'w') as fhd:
            json.dump(obj, fhd, indent=4)

    return obj
