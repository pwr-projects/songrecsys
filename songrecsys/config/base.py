class ConfigBase:

    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    @property
    def base_dict(self) -> dict:
        return self.__dict__
