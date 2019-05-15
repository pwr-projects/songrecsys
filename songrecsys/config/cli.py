from argparse import ArgumentParser
from typing import *

from songrecsys.config.base import *

__all__ = ['ConfigCLI']


class ConfigCLI(ConfigBase):

    def __init__(self, *args, **kwargs):
        parser = ArgumentParser(description='Song recommendation system')
        parser.add_argument('--spotify_id', type=str, help='Spotify app client id')
        parser.add_argument('--spotify_secret', type=str, help='Spotify app client secret')
        parser.add_argument('--genius_id', type=str, help='Genius app client id')
        parser.add_argument('--genius_secret', type=str, help='Genius app client secret')
        parser.add_argument('--request_interval', type=float, help='Interval between API requests', default=0.1)

        args = parser.parse_args()
        super().__init__(**(args.__dict__))
