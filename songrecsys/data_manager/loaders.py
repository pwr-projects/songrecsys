import json
import pickle
from collections import namedtuple
from pathlib import Path
from typing import *

__all__ = ['load_from_json', 'load_from_pickle']


def load_from_pickle(where: Path, verbose=False):
    if verbose:
        print(f'Loading pickle from {where}', end='... ')

    with open(where, 'rb') as fhd:
        return pickle.load(fhd, fix_imports=True)


def load_from_json(where: Union[Path, str], convert_to_object=False, verbose=False) -> Dict[str, Any]:
    if verbose:
        print(f'Loading json from {where}', end='... ')

    object_hook = None

    if convert_to_object:
        object_hook = lambda json_obj: namedtuple('Data', json_obj.keys())(*json_obj.values())
    else:
        object_hook = None

    with open(where, 'r', encoding='utf-8') as fhd:
        return json.load(fhd, object_hook=object_hook)
