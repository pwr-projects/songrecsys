import json
from pathlib import Path
from typing import *

from songrecsys.config.base import *
from songrecsys.data_manager import *

__all__ = ['ConfigJSON']


class ConfigJSON(ConfigBase):

    def __init__(self, path: Union[Path, str], *args, **kwargs):
        conf = load_from_json(path)
        conf['request_interval'] = conf.get('request_interval', 100) / 1000
        super().__init__(**conf)
