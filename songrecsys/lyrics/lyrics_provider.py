from abc import ABC, abstractmethod
from time import sleep
from typing import Dict

from songrecsys.config.base import ConfigBase
from songrecsys.data.manager import DataFormat, dump
from songrecsys.utils.utils import tqdm
from songrecsys.schemes import Data


class LyricsProvider(ABC):

    def __init__(self, config: ConfigBase):
        self.verbose = config.verbose if hasattr(config, 'verbose') else False

    @abstractmethod
    def get(self, title, artist):
        ...

    def download_lyrics(self, data: Data, save_interval: int = 20, save_data_format: DataFormat = DataFormat.pickle) -> Dict[str, str]:
        interval_cnt = 0
        with tqdm(data.tracks.items(), 'Adding lyrics to tracks') as pbar:
            for idx, track in pbar:
                if not track.lyrics:
                    pbar.set_description(f'{save_interval - interval_cnt}/{save_interval}')
                    got = False
                    while not got:
                        try:
                            track.lyrics = self.get(track.title.replace('(', '').replace(')', ''), ' '.join(track.artists))
                            got = True
                            interval_cnt += 1
                        except:
                            pbar.set_description('Trying again')
                            sleep(2)

                if interval_cnt == save_interval:
                    pbar.set_description('Saving')
                    dump(merged_data=data, data_format=save_data_format)
                    interval_cnt = 0

            dump(merged_data=data, data_format=save_data_format)
        return data
