from typing import *

from songrecsys.data_manager.loaders import *
from songrecsys.data_manager.savers import *

__all__ = ['DataFormat']


class DataFormat:
    json = 0
    pickle = 1

    saver: Dict[int, Callable] = {json: save_to_json, pickle: save_to_pickle}
    loader: Dict[int, Callable] = {json: load_from_json, pickle: load_from_pickle}

    @staticmethod
    def is_valid(val: int):
        assert val in (DataFormat.pickle, DataFormat.json), 'data_format has to have value from DataFormat'
