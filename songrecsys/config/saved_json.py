import json
from pathlib import Path
from songrecsys.data import load_from_json
from songrecsys.config.base import ConfigBase


class ConfigJSON(ConfigBase):

    def __init__(self, path: Path, *args, **kwargs):
        conf = load_from_json(path)
        if conf.get('request_interval'):
            conf['request_interval'] = conf.get('request_interval') / 1000
        super().__init__(**conf)

    @property
    def base_dict(self) -> dict:
        return super().base_dict
