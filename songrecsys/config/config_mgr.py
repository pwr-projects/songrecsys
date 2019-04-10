import json
import sys
from typing import NoReturn, Text

from ..consts import DEFAULT_PATH_CONFIG
from .base import ConfigBase
from .cli import ConfigCLI
from .interactive import ConfigInteractive
from .saved_json import ConfigJSON


class ConfigMgr:
    def __init__(self, config_path: Text = DEFAULT_PATH_CONFIG, *args, **kwargs):
        self._config_path = config_path
        self._config = self.load()
        self._setattrs()
        self.dump()

    def _setattrs(self) -> NoReturn:
        for k, v in self._config.base_dict.items():
            setattr(self, k, v)

    def load(self) -> ConfigBase:
        if len(sys.argv) != 1:
            return ConfigCLI()

        if ConfigJSON.exists(self._config_path):
            return ConfigJSON(self._config_path)

        return ConfigInteractive()

    def dump(self) -> NoReturn:
        with open(self._config_path, 'w') as fhd:
            json.dump(self._config.base_dict, fhd, indent=4)
