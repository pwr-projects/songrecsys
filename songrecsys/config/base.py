from typing import *

__all__ = ['ConfigBase', 'AnyConfig']

AnyConfig = TypeVar('AnyConfig', bound='ConfigBase')


class ConfigBase:

    def __init__(self, **kwargs):
        self.base_dict.update(kwargs)

    @property
    def base_dict(self):
        return self.__dict__
