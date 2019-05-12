import json
from pathlib import Path

from songrecsys.config.base import *
from songrecsys.data import *

__all__ = ['ConfigJSON']


class ConfigJSON(ConfigBase):

    def __init__(self, path: Path, *args, **kwargs):
        conf = load_from_json(path)
        if conf.get('request_interval'):
            conf['request_interval'] = conf.get('request_interval') / 1000
        super().__init__(**conf)

    @property
    def base_dict(self) -> dict:
        return super().base_dict
