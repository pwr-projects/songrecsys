from typing import Dict, Sequence, Text

import numpy as np
import spotipy.util as util
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.util import prompt_for_user_token
from tqdm import tqdm

from songrecsys.config import ConfigBase

from .playlist_mgr import PlaylistMgr


class SpotifyWrapper(Spotify):
    def __init__(self, config: ConfigBase, username: Text, *args, **kwargs):
        """Spotipy wrapper allowing to perform operations on playlists and so on

        Arguments:
            Spotify {class} -- Spotify API by spotipy
            config {ConfigBase} -- Config schema    
            username {Text} -- name of user used for scraper
        """

        auth = SpotifyClientCredentials(client_id=config.config.spotify_id,
                                        client_secret=config.config.spotify_secret)
        super().__init__(client_credentials_manager=auth,
                         *args, **kwargs)

        self._username = username
        self._playlist_mgr = PlaylistMgr(self)

    @property
    def username(self):
        return self._username

    @property
    def pl(self) -> PlaylistMgr:
        """Getter for playlist manager

        Returns:
            PlaylistMgr -- PlaylistMgr instance
        """
        return self._playlist_mgr
