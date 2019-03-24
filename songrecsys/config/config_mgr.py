import json
import sys
from typing import Text

from ..consts import CONFIG_DEFAULT_PATH
from .base import ConfigBase
from .cli import ConfigCLI
from .interactive import ConfigInteractive
from .saved_json import ConfigJSON


class ConfigMgr:

    def __init__(self, config_path: Text = CONFIG_DEFAULT_PATH, *args, **kwargs):
        self._config_path = config_path
        self.config = self.load()
        self.dump()

    @classmethod
    def has_args(cls) -> bool:
        return len(sys.argv) != 1

    def load(self) -> ConfigBase:
        if self.has_args():
            return ConfigCLI()

        if ConfigJSON.exists(self._config_path):
            return ConfigJSON(self._config_path)

        return ConfigInteractive()

    def dump(self):
        with open(self._config_path, 'w') as fhd:
            json.dump(self.config.base_dict, fhd, indent=4)
