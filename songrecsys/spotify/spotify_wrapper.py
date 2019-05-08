from typing import List

from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

from songrecsys.config import ConfigBase


class SpotifyWrapper(Spotify):

    def __init__(self, config: ConfigBase, usernames: List[str], *args, **kwargs):
        '''Spotipy wrapper allowing to perform operations on playlists and so on

        Arguments:
            Spotify {class} -- Spotify API by spotipy
            config {ConfigBase} -- Config schema
            username {Text} -- name of user used for scraper
        '''

        auth = SpotifyClientCredentials(client_id=config.spotify_id, client_secret=config.spotify_secret)
        super().__init__(client_credentials_manager=auth, *args, **kwargs)
        self._usernames = usernames

    @property
    def usernames(self) -> List[str]:
        return self._usernames
