from typing import Text


class ConfigBase:
    def __init__(self,
                 spotify_id: Text,
                 spotify_secret: Text):
        self.client_id = spotify_id
        self.client_secret = spotify_secret

    @property
    def base_dict(self):
        return self.__dict__
