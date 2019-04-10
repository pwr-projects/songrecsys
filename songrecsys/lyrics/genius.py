from typing import Dict, Sequence, Text

import lyricsgenius
from tqdm import tqdm

from songrecsys.config import ConfigBase
from songrecsys.consts import DEFAULT_PATH_PLAYLISTS
from songrecsys.utils.json_func import save_to_json


class LyricsGenius(lyricsgenius.Genius):
    def __init__(self, config: ConfigBase):
        super().__init__(config.genius_id)
        self.verbose = config.verbose if hasattr(config, 'verbose') else False

    def lyrics(self, title: Text, artist: Text) -> Text:
        lyrics_info = self.search_song(title, artist, False)
        return lyrics_info.lyrics if lyrics_info else None

    def add_lyrics_to_dataset(self, pl_infos: Sequence[Dict]) -> Sequence[Dict]:
        for pl_info in tqdm(pl_infos, 'Adding lyrics to playlists', leave=False):
            for track_info in tqdm(pl_info['tracks'], 'Adding lyrics to tracks', leave=False):
                track_info['lyrics'] = self.lyrics(track_info['title'], ' '.join(track_info['artists']))
        save_to_json(pl_infos, DEFAULT_PATH_PLAYLISTS)
        return pl_infos
