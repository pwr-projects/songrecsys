from typing import Text

from lyricwikia import LyricsNotFound, get_lyrics

from songrecsys.config.base import ConfigBase
from songrecsys.lyrics.lyrics_provider import LyricsProvider


class LyricWikia(LyricsProvider):
    def __init__(self, config: ConfigBase):
        LyricsProvider.__init__(self, config)

    def get(self,
            title: Text,
            artist: Text) -> Text:
        lyrics = None
        try:
            lyrics = get_lyrics(artist, title)
        except LyricsNotFound:
            pass
        finally:
            return lyrics

    def add_lyrics_to_dataset(self, **kwargs):
        return LyricsProvider.add_lyrics_to_dataset(**kwargs, getter_func=self.get)