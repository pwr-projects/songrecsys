from .base import ConfigBase


class ConfigInteractive(ConfigBase):
    def __init__(self,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        raise NotImplementedError
