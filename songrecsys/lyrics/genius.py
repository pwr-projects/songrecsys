from time import sleep
from typing import Dict, Sequence

from lyricsgenius.api import Genius

from songrecsys.config import ConfigBase
from songrecsys.data import dump
from songrecsys.lyrics.lyrics_provider import LyricsProvider
from songrecsys.schemes import Track
from songrecsys.utils import tqdm


class LyricsGenius(Genius, LyricsProvider):

    def __init__(self, config: ConfigBase):
        Genius.__init__(self, config.genius_id)
        LyricsProvider.__init__(self, config)

    def get(self, title: str, artist: str) -> str:
        lr = self.search_song(title, artist, False)
        return lr.lyrics if lr else None
