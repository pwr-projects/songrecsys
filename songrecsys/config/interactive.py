from songrecsys.config.base import *

__all__ = ['ConfigInteractive']


class ConfigInteractive(ConfigBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        raise NotImplementedError
