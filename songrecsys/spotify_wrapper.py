import spotipy.util as util
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.util import prompt_for_user_token

from .config import ConfigBase


class SpotifyWrapper(Spotify):
    def __init__(self, config: ConfigBase, *args, **kwargs):
        auth = SpotifyClientCredentials(client_id=config.config.client_id,
                                        client_secret=config.config.client_secret)
        super().__init__(client_credentials_manager=auth,
                         *args, **kwargs)


# ['user-read-private', 'user-read-birthdate', 'user-read-email', 'playlist-read-private', 'user-library-read', 'user-library-modify', 'user-top-read', 'playlist-read-collaborative', 'playlist-modify-public',
#     'playlist-modify-private', 'user-follow-read', 'user-follow-modify', 'user-read-currently-playing', 'user-modify-playback-state', 'user-read-recently-played', 'user-read-playback-state']
