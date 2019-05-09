import multiprocessing as mp
from abc import ABC, abstractmethod
from itertools import zip_longest
from sys import stdout
from time import sleep
from typing import Dict

from songrecsys.config import ConfigBase
from songrecsys.data import DataFormat, dump
from songrecsys.multiprocessing import mp_lyrics_downloader
from songrecsys.schemes import Data
from songrecsys.utils import grouper, tqdm


class LyricsProvider(ABC):

    def __init__(self, config: ConfigBase):
        self.verbose = getattr(config, 'verbose', False)

    @abstractmethod
    def get(self, title, artist):
        ...

    def download_lyrics(self, data: Data, save_interval: int = 50) -> Data:
        # interval_cnt = 0
        to_download = set((filter(lambda track: not data.tracks[track].lyrics, data.tracks)))
        for group in grouper(to_download, save_interval):
            before = len(tuple(filter(lambda track: not track.lyrics, data.tracks.values())))
            with mp.Pool(mp.cpu_count()) as pool:
                tracks = pool.starmap(mp_lyrics_downloader, [(track, data.tracks[track], [
                    data.artists[art_id].name for art_id in data.tracks[track].artists_ids if data.artists.get(art_id)
                ], self.get) for track in group])
                for track_id, track in tracks:
                    data.tracks[track_id] = track
            after = len(tuple(filter(lambda track: not track.lyrics, data.tracks.values())))
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
            print('Downloaded', before - after, 'lyrics.', after, 'to finish.')
            dump(data)
        return data
