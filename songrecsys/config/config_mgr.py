from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import *

from songrecsys.config.base import *
from songrecsys.config.cli import *
from songrecsys.config.interactive import *
from songrecsys.config.saved_json import *
from songrecsys.consts import *
from songrecsys.data_manager import *

__all__ = ['ConfigMgr', 'ConfigBase']


class ConfigMgr:

    def __init__(self, config_path: Union[Path, str] = FILEPATH_PATH_CONFIG, *args, **kwargs):
        self._config_path = config_path
        self._config: ConfigBase = self.load()
        self._setattrs()
        self.dump()

    @property
    def config(self) -> Dict[str, Any]:
        return self._config.base_dict

    def _setattrs(self) -> NoReturn:
        for k, v in self._config.base_dict.items():
            setattr(self, k, v)

    def load(self) -> ConfigBase:
        # ipython = False
        # try:
        #     from IPython import get_ipython
        #     cfg = get_ipython().config
        #     if cfg['IPKernelApp']['parent_appname'] == 'ipython-notebook':
        #         ipython = True
        # except:
        #     ...

        # try:
        #     if not ipython and len(sys.argv) > 1:
        #         return ConfigCLI()
        # except:
        #     ...

        if Path(self._config_path).exists():
            print(f'Loading config from {self._config_path}')
            return ConfigJSON(self._config_path)

        return ConfigInteractive()

    def dump(self) -> ConfigMgr:
        conf = self._config.base_dict.copy()
        conf['request_interval'] = conf['request_interval'] * 1000
        save_to_json(conf, self._config_path)
        return self
