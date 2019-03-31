from argparse import ArgumentParser

from .base import ConfigBase


class ConfigCLI(ConfigBase):
    def __init__(self, *args, **kwargs):
        parser = ArgumentParser(description='Song recommendation system')
        parser.add_argument('--spotify_id',  type=str, help='Spotify app client')
        parser.add_argument('--spotify_secret', type=str, help='Spotify app secret')

        args = parser.parse_args()
        super().__init__(*args.__dict__.values())

    @property
    def base_dict(self):
        return super().base_dict