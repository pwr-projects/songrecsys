from typing import Text


class ConfigBase:
    def __init__(self,
                 spotify_id: Text,
                 spotify_secret: Text):
        self.spotify_id = spotify_id
        self.spotify_secret = spotify_secret

    @property
    def base_dict(self):
        return self.__dict__
