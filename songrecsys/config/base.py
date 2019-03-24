from typing import Text


class ConfigBase:
    def __init__(self, 
    client_id: Text,
                 client_secret: Text):
        self.client_id = client_id
        self.client_secret = client_secret

    @property
    def base_dict(self):
        return self.__dict__
