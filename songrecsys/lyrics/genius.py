from time import sleep
from typing import Dict, Sequence, Text

from lyricsgenius.api import Genius

from songrecsys.config.base import ConfigBase
from songrecsys.lyrics.lyrics_provider import LyricsProvider
from songrecsys.schemes import Track


class LyricsGenius(Genius, LyricsProvider):
    def __init__(self, config: ConfigBase):
        Genius.__init__(self, config.genius_id)
        LyricsProvider.__init__(self, config)

    def get(self,
            title: Text,
            artist: Text) -> Text:
        lr = self.search_song(title, artist, False)
        return lr.lyrics if lr else None

    def add_lyrics_to_dataset(self,
                              tracks: Dict[Text, Track],
                              save_interval: int = 20) -> Dict[Text, Track]:
        interval_cnt = 0
        for idx, track in tqdm(tracks.items(), 'Adding lyrics to tracks', leave=False):
            if not track.lyrics:
                got = False
                while not got:
                    try:
                        tracks[idx].lyrics = self.lyrics(track.title, ' '.join(track.artists))
                        got = True
                    except:
                        print('Wait and try again...')
                        sleep(2)
                interval_cnt += 1
            if interval_cnt == save_interval:
                dump(tracks=tracks, verbose=False)
                interval_cnt = 0
        return tracks
