from argparse import ArgumentParser

from .base import ConfigBase


class ConfigCLI(ConfigBase):
    def __init__(self, *args, **kwargs):
        parser = ArgumentParser(description='Song recommendation system')
        parser.add_argument('--spotify_id', type=str,
                            help='Spotify app client id')
        parser.add_argument('--spotify_secret', type=str,
                            help='Spotify app client secret')
        parser.add_argument('--genius_id', type=str,
                            help='Genius app client id')
        parser.add_argument('--genius_secret', type=str,
                            help='Genius app client secret')

        args = parser.parse_args()
        super().__init__(**args.__dict__)

    @property
    def base_dict(self):
        return super().base_dict
