import json
from pathlib import Path


def save_to_json(obj: object,
                 where: Path,
                 default_override: bool = True) -> object:
    override = True
    if not default_override and where.exists():
        answer = input(f'{where} exists. Override? [Yy/Nn] ')
        override = answer in 'YyTt'

    if override:
        with open(where, 'w') as fhd:
            json.dump(obj, fhd, indent=4, default=lambda obj: obj.__dict__)
    return obj


def load_from_json(where: Path) -> object:
    with open(where, 'r') as fhd:
        return json.load(fhd)
