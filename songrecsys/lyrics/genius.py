from time import sleep
from typing import Dict, Sequence

from lyricsgenius.api import Genius

from songrecsys.config import *
from songrecsys.data import *
from songrecsys.lyrics.lyrics_provider import *
from songrecsys.schemes import *
from songrecsys.misc import *

__all__ = ['LyricsGenius']


class LyricsGenius(Genius, LyricsProvider):

    def __init__(self, config: ConfigBase):
        Genius.__init__(self, getattr(config, 'genius_id'))
        LyricsProvider.__init__(self, config)

    def get(self, title: str, artist: str) -> str:
        lr = self.search_song(title, artist, False)
        return lr.lyrics if lr else None
