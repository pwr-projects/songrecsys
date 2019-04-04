from typing import Text

import lyricsgenius

from songrecsys.config import ConfigBase


class LyricsGenius(lyricsgenius.Genius):
    def __init__(self, config: ConfigBase):
        super().__init__(config.genius_access_token)
        self.verbose = config.verbose

    def lyrics(self, title: Text, artist: Text) -> Text:
        lyrics_info = self.search_song(title, artist, False)
        return lyrics_info if lyrics_info else None
