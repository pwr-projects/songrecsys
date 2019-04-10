import json
from os.path import exists
from typing import Dict, Text

from .base import ConfigBase


class ConfigJSON(ConfigBase):
    def __init__(self, path: Text, *args, **kwargs):
        super().__init__(**self.load(path))

    @property
    def base_dict(self) -> Dict:
        return super().base_dict

    @classmethod
    def load(cls, path: Text) -> Dict:
        with open(path, 'r') as fhd:
            return json.load(fhd)

    @classmethod
    def exists(cls, path: Text) -> bool:
        return exists(path)
