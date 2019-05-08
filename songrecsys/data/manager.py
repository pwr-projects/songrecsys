import json
import pickle
from collections import namedtuple
from enum import auto
from pathlib import Path
from typing import Dict, NoReturn, Tuple

from pandas import DataFrame

from songrecsys.consts import DEFAULT_PATH_MERGED_DATA
from songrecsys.schemes import Data, Playlist, Track
from songrecsys.utils import override_prompt, tqdm


def save_to_pickle(what: object, where: Path, default_override: bool = True, verbose: bool = False) -> object:
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
        return pickle.load(fhd)


def save_to_json(what: object, where: Path, default_override: bool = True, verbose: bool = False) -> object:
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

    if convert_to_object:
        object_hook = lambda json_obj: namedtuple('Data', json_obj.keys())(*json_obj.values())
    else:
        object_hook = None

    with open(where, 'r', encoding='utf-8') as fhd:
        return json.load(fhd, object_hook=object_hook)


class DataFormat:
    json = auto()
    pickle = auto()

    saver = {json: save_to_json, pickle: save_to_pickle}
    loader = {json: load_from_json, pickle: load_from_pickle}


def dump(data: Data, data_format: DataFormat = DataFormat.pickle, verbose: bool = True,
         default_override: bool = True) -> NoReturn:
    saver = DataFormat.saver.get(data_format)
    try:
        saver(data, DEFAULT_PATH_MERGED_DATA, default_override, verbose)
        if verbose:
            print('OK')
    except Exception as e:
        if verbose:
            print(f'FAILED: {e}')
    return data


def load(data_format: DataFormat = DataFormat.pickle, verbose: bool = True) -> Data:
    loader = DataFormat.loader.get(data_format)
    try:
        data = loader(DEFAULT_PATH_MERGED_DATA, verbose)
        if data_format == DataFormat.json:
            data = Data.from_json(data)
        print('OK')
        return data
    except Exception as e:
        print(f'FAILED: {e}')
        return Data()
