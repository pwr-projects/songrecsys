import json
from pathlib import Path
from songrecsys.data import load_from_json
from songrecsys.config.base import ConfigBase


class ConfigJSON(ConfigBase):

    def __init__(self, path: Path, *args, **kwargs):
        super().__init__(**load_from_json(path))

    @property
    def base_dict(self) -> dict:
        return super().base_dict
