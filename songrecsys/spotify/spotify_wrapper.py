from typing import *

from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

from songrecsys.config import ConfigBase
from songrecsys.misc import desc_task_begin, desc_task_end

__all__ = ['SpotifyWrapper']


class SpotifyWrapper(Spotify):

    def __init__(self, config: ConfigBase, usernames: Iterable[str], *args, **kwargs):
        '''Spotipy wrapper allowing to perform operations on playlists and so on

        Arguments:
            Spotify {class} -- Spotify API by spotipy
            config {ConfigBase} -- Config schema
            username {Text} -- name of user used for scraper
        '''

        auth = SpotifyClientCredentials(client_id=getattr(config, 'spotify_id'),
                                        client_secret=getattr(config, 'spotify_secret'))
        super().__init__(client_credentials_manager=auth, *args, **kwargs)
        self.usernames = usernames

    def get_valid_users(self):
        for user_id in self.usernames:
            try:
                desc_task_begin(f'Checking user of id: {user_id}')
                self.user(user_id)
                desc_task_end('OK')
            except:
                desc_task_end('FAIL')
