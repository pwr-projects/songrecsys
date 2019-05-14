from typing import *

from songrecsys.consts import *
from songrecsys.data_manager.data_format import *
from songrecsys.schemes import *

__all__ = ['dump', 'load']


def dump(data: Data, data_format: int = DataFormat.pickle, verbose: bool = True, default_override: bool = True) -> Data:
    DataFormat.is_valid(data_format)
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
    DataFormat.is_valid(data_format)
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
