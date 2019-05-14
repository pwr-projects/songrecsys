import json
import pickle
from pathlib import Path
from typing import *

from songrecsys.misc import *

__all__ = ['save_to_json', 'save_to_pickle']


def save_to_pickle(what: T, where: Union[str, Path], defaulToverride: bool = True, verbose: bool = False) -> T:
    if verbose:
        print(f'Saving data to {where}', end='... ')
    if override_prompt(defaulToverride, where):
        with open(where, 'wb') as fhd:
            pickle.dump(what, fhd)
    return what


def save_to_json(what: T, where: Union[str, Path], defaulToverride: bool = True, verbose: bool = False) -> T:
    if not str(where).endswith('.json'):
        where = str(where) + '.json'

    if verbose:
        print(f'Saving data to {where}', end='... ')

    if override_prompt(defaulToverride, where):
        with open(where, 'w', encoding='utf-8') as fhd:
            # # Uncomment to use "stream" mode
            # for chunk in tqdm(json.JSONEncoder(default=lambda obj: obj.__dict__).iterencode(what)):
            #     fhd.write(chunk + '\n')
            json.dump(what, fhd, indent=4, default=lambda obj: list(obj) if isinstance(obj, set) else obj.__dicT_)
    return what
