import json
from os import sys
from pathlib import Path
from typing import NoReturn

from songrecsys.config.base import ConfigBase
from songrecsys.config.cli import ConfigCLI
from songrecsys.config.interactive import ConfigInteractive
from songrecsys.config.saved_json import ConfigJSON
from songrecsys.consts import DEFAULT_PATH_CONFIG
from songrecsys.data import save_to_json


class ConfigMgr:

    def __init__(self, config_path: Path = DEFAULT_PATH_CONFIG, *args, **kwargs):
        self._config_path = config_path
        self._config = self.load()
        self._setattrs()
        self.dump()

    def _setattrs(self) -> NoReturn:
        for k, v in self._config.base_dict.items():
            setattr(self, k, v)

    def load(self) -> ConfigBase:
        try:
            if len(sys.argv) > 1:
                return ConfigCLI()
        except:
            ...

        if Path(self._config_path).exists():
            return ConfigJSON(self._config_path)

        return ConfigInteractive()

    def dump(self) -> object:
        save_to_json(self._config.base_dict, self._config_path)
        return self
