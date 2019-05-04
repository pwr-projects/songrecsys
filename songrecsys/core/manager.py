from typing import List

from songrecsys.config import ConfigMgr
from songrecsys.lyrics import LyricsProvider
from songrecsys.schemes import Data
from songrecsys.spotify import ArtistsDownloader, PlaylistMgr, SpotifyWrapper


class Manager:

    def __init__(self, usernames: List[str], lyrics_source: LyricsProvider, data: Data = Data()):
        self._config = ConfigMgr()
        self._sp = SpotifyWrapper(self.config, usernames)
        self._lp = lyrics_source(self.config)
        self._pl = PlaylistMgr(self._sp, data)
        self._ad = ArtistsDownloader(self._sp, data)

    @property
    def config(self):
        return self._config

    @property
    def sp(self):
        return self._sp

    @property
    def spotify(self):
        return self.sp

    @property
    def lp(self):
        return self._lp

    @property
    def lyrics(self):
        return self.lp

    @property
    def pl(self):
        return self._pl

    @property
    def playlist(self):
        return self.pl

    @property
    def ad(self):
        return self._ad

    @property
    def artists(self):
        return self._ad
