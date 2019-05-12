from typing import List

from songrecsys.config import *
from songrecsys.lyrics import *
from songrecsys.schemes import *
from songrecsys.spotify import *

__all__ = ['Manager']


class Manager:

    def __init__(self,
                 usernames: List[str],
                 lyrics_source = LyricsGenius,
                 data: Data = Data(),
                 override: bool = True):
        self._config = ConfigMgr()
        self._sp = SpotifyWrapper(self.config, usernames)
        self._lp = lyrics_source(self.config)
        self._pl = PlaylistMgr(self._sp, self._config, data, override)
        self._ad = ArtistsDownloader(self._sp, self.config, data)
        self._data = data

    @property
    def config(self):
        return self._config

    @property
    def data(self) -> Data:
        return self._data

    @property
    def sp(self) -> SpotifyWrapper:
        return self._sp

    @property
    def spotify(self) -> SpotifyWrapper:
        return self.sp

    @property
    def lp(self) -> LyricsProvider:
        return self._lp

    @property
    def lyrics(self) -> LyricsProvider:
        return self.lp

    @property
    def pl(self) -> PlaylistMgr:
        return self._pl

    @property
    def playlist(self) -> PlaylistMgr:
        return self.pl

    @property
    def ad(self) -> ArtistsDownloader:
        return self._ad

    @property
    def artists(self) -> ArtistsDownloader:
        return self._ad
