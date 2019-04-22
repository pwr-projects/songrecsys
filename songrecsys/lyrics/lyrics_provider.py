from abc import ABC, abstractmethod
from pprint import pprint
from time import sleep
from typing import Callable, Dict, Text

from tqdm.auto import tqdm

from songrecsys.config.base import ConfigBase
from songrecsys.data import dump, load
from songrecsys.data.manager import DataFormat
from songrecsys.schemes.track import Track


class LyricsProvider(ABC):
    def __init__(self, config: ConfigBase):
        self.verbose = config.verbose if hasattr(config, 'verbose') else False

    @abstractmethod
    def get(self, title, artist):
        ...

    def download_lyrics(self,
                        tracks: Dict[Text, Track],
                        lyrics: Dict[Text, Text] = {},
                        save_interval: int = 20) -> Dict[Text, Track]:
        interval_cnt = 0
        with tqdm(tracks.items(), 'Adding lyrics to tracks') as pbar:
            for idx, track in pbar:
                if idx not in lyrics.keys():
                    pbar.set_description(' '.join([f'{save_interval - interval_cnt}/{save_interval}',
                                                   f'{track.artists} - {track.title}']))
                    got = False
                    while not got:
                        try:

                            lyrics[idx] = self.get(track.title.replace('(', '').replace(')', ''),
                                                   ' '.join(track.artists))
                            got = True
                            interval_cnt += 1
                        except:
                            pbar.set_description('Trying again')
                            sleep(2)
                if interval_cnt == save_interval:
                    pbar.set_description('Saving')
                    dump(lyrics=lyrics)
                    interval_cnt = 0
            dump(lyrics=lyrics)
        return lyrics
