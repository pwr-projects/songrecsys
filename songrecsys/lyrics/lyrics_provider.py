from abc import ABC, abstractmethod
from time import sleep
from typing import Dict, Text

from tqdm.auto import tqdm

from songrecsys.config.base import ConfigBase
from songrecsys.schemes.track import Track
from songrecsys.data import dump, load


class LyricsProvider(ABC):
    def __init__(self, config: ConfigBase):
        self.verbose = config.verbose if hasattr(config, 'verbose') else False

    @abstractmethod
    def get(self, title, artist):
        ...

    def add_lyrics_to_dataset(self,
                              tracks: Dict[Text, Track],
                              save_interval: int = 20) -> Dict[Text, Track]:
        interval_cnt = 0
        for idx, track in tqdm(tracks.items(), 'Adding lyrics to tracks', leave=False):
            if not track.lyrics:
                got = False
                while not got:
                    try:
                        tracks[idx].lyrics = self.get(track.title, ' '.join(track.artists))
                        got = True
                    except:
                        print('Wait and try again...')
                        sleep(2)
                interval_cnt += 1
            if interval_cnt == save_interval:
                dump(tracks=tracks, verbose=False)
                interval_cnt = 0
        return tracks
