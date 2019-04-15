from typing import Dict, Sequence, Text

import lyricsgenius
from tqdm.auto import tqdm

from songrecsys.config import ConfigBase
from songrecsys.consts import DEFAULT_PATH_TRACKS
from songrecsys.schemes.track import Track
from songrecsys.utils.json_func import dump, save_to_json


class LyricsGenius(lyricsgenius.Genius):
    def __init__(self, config: ConfigBase):
        super().__init__(config.genius_id)
        self.verbose = config.verbose if hasattr(config, 'verbose') else False

    def lyrics(self, title: Text, artist: Text) -> Text:
        lr = self.search_song(title, artist, False)
        return lr.lyrics if lr else None

    def add_lyrics_to_dataset(self,
                              tracks: Dict[Text, Track],
                              save_interval: int = 5) -> Dict[Text, Track]:
        interval_cnt = 0
        for idx in tqdm(tracks, 'Adding lyrics to tracks', leave=False):
            if not tracks[idx].lyrics:
                tracks[idx].lyrics = self.lyrics(tracks[idx].title, ' '.join(tracks[idx].artists))
                interval_cnt += 1
            if interval_cnt == save_interval:
                dump(tracks=tracks, verbose=False)
                interval_cnt = 0
        return tracks
