from typing import Dict, Text


class ConfigBase:
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    @property
    def base_dict(self) -> Dict:
        return self.__dict__
