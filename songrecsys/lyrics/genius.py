from time import sleep
from typing import Dict, Sequence, Text

from lyricsgenius.api import Genius

from songrecsys.config.base import ConfigBase
from songrecsys.lyrics.lyrics_provider import LyricsProvider
from songrecsys.schemes import Track
from songrecsys.utils.utils import tqdm
from songrecsys.data.manager import dump


class LyricsGenius(Genius, LyricsProvider):
    def __init__(self, config: ConfigBase):
        Genius.__init__(self, config.genius_id)
        LyricsProvider.__init__(self, config)

    def get(self,
            title: Text,
            artist: Text) -> Text:
        lr = self.search_song(title, artist, False)
        return lr.lyrics if lr else None
