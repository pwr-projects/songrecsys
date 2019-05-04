from abc import ABC, abstractmethod
from time import sleep
from typing import Dict
import multiprocessing as mp
from songrecsys.config.base import ConfigBase
from songrecsys.data.manager import DataFormat, dump
from songrecsys.utils.utils import tqdm
from songrecsys.schemes import Data
from sys import stdout


def downloader(track, getter):
    artists = ', '.join(track.artists)
    what = f'{artists} - {track.title}'
    stdout.write(f'Downloading {what}\n')
    
    stdout.flush()
    got = False
    while not got:
        try:
            track.lyrics = getter(track.title.replace('(', '').replace(')', ''), ' '.join(track.artists))
            got = True
        except:
            sleep(2)
    if track.lyrics:
        stdout.write(f'Downloaded  {what}\n')
        stdout.flush()


class LyricsProvider(ABC):

    def __init__(self, config: ConfigBase):
        self.verbose = config.verbose if hasattr(config, 'verbose') else False

    @abstractmethod
    def get(self, title, artist):
        ...

    def download_lyrics(self, data: Data, save_interval: int = 20) -> Data:
        interval_cnt = 0
        to_download = tuple(filter(lambda track: not track.lyrics, data.tracks.values()))
        with mp.Pool(mp.cpu_count()) as pool:
            pool.starmap(downloader, [(track, self.get) for track in to_download])

            # for track in pbar:
            #     pbar.set_description(f'{save_interval - interval_cnt}/{save_interval}')
            #     got = False
            #     while not got:
            #         try:
            #             track.lyrics = self.get(track.title.replace('(', '').replace(')', ''), ' '.join(track.artists))
            #             got = True
            #             interval_cnt += 1
            #         except:
            #             pbar.set_description('Trying again')
            #             sleep(2)

            #     if interval_cnt == save_interval:
            #         pbar.set_description('Saving')
            #         dump(data, verbose=False)
            #         interval_cnt = 0

            dump(data)
        return data