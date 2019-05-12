import json
import pickle
from collections import namedtuple
from enum import auto
from pathlib import Path
from typing import Any, Callable, Dict, NoReturn, Optional, Tuple, Union

from pandas import DataFrame

from songrecsys.consts import *
from songrecsys.schemes import *
from songrecsys.misc import *

__all__ = ['save_to_json', 'load_from_json', 'save_to_pickle', 'load_from_pickle', 'DataFormat', 'dump', 'load']


def save_to_pickle(what: object, where: Union[Path, str], default_override: bool = True,
                   verbose: bool = False) -> object:
    if verbose:
        print(f'Saving data to {where}', end='... ')
    if override_prompt(default_override, where):
        with open(where, 'wb') as fhd:
            pickle.dump(what, fhd)
    return what


def load_from_pickle(where: Path, verbose: bool = False):
    if verbose:
        print(f'Loading pickle from {where}', end='... ')

    with open(where, 'rb') as fhd:
        return pickle.load(fhd, fix_imports=True)


def save_to_json(what: object, where: Union[Path, str], default_override: bool = True, verbose: bool = False) -> object:
    if not str(where).endswith('.json'):
        where = str(where) + '.json'

    if verbose:
        print(f'Saving data to {where}', end='... ')

    if override_prompt(default_override, where):
        with open(where, 'w', encoding='utf-8') as fhd:
            # # Uncomment to use "stream" mode
            # for chunk in tqdm(json.JSONEncoder(default=lambda obj: obj.__dict__).iterencode(what)):
            #     fhd.write(chunk + '\n')
            json.dump(what, fhd, indent=4, default=lambda obj: list(obj) if isinstance(obj, set) else obj.__dict__)
    return what


def load_from_json(where: Path, convert_to_object: bool = False, verbose: bool = False):
    if verbose:
        print(f'Loading json from {where}', end='... ')

    object_hook: Optional[Callable] = None

    if convert_to_object:
        object_hook = lambda json_obj: namedtuple('Data', json_obj.keys())(*json_obj.values())
    else:
        object_hook = None

    with open(where, 'r', encoding='utf-8') as fhd:
        return json.load(fhd, object_hook=object_hook)


class DataFormat:
    json = 0
    pickle = 1

    saver: Dict[int, Callable] = {json: save_to_json, pickle: save_to_pickle}
    loader: Dict[int, Callable] = {json: load_from_json, pickle: load_from_pickle}


def dump(data: Data, data_format: int = DataFormat.pickle, verbose: bool = True, default_override: bool = True) -> Data:
    saver = DataFormat.saver[data_format]
    try:
        saver(data, FILEPATH_DATA_PICKLED, default_override, verbose)
        if verbose:
            print('OK')
    except Exception as e:
        if verbose:
            print(f'FAILED: {e}')
    return data


def load(data_format: int = DataFormat.pickle, verbose: bool = True) -> Data:
    loader = DataFormat.loader[data_format]
    try:
        data = loader(FILEPATH_DATA_PICKLED, verbose)
        if data_format == DataFormat.json:
            data = Data.from_json(data)
        print('OK')
        return data
    except Exception as e:
        print(f'FAILED: {e}')
        return Data()
