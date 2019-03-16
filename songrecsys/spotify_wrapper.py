from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyWrapper(Spotify):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
