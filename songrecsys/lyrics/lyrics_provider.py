import multiprocessing as mp
from abc import ABC, abstractmethod
from itertools import zip_longest
from sys import stdout
from time import sleep
from typing import *

from songrecsys.config import *
from songrecsys.data_manager import *
from songrecsys.misc import *
from songrecsys.multiprocessing import *
from songrecsys.schemes import *

__all__ = ['LyricsProvider', 'AnyLyrics']

AnyLyrics = TypeVar('AnyLyrics', bound='LyricsProvider')


class LyricsProvider(ABC):

    def __init__(self, config: ConfigBase):
        self.verbose: bool = getattr(config, 'verbose', False)

    @abstractmethod
    def get(self, title: str, artist: str) -> Optional[str]:
        raise NotImplementedError

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
            print('Downloaded', before - after, 'lyrics.', after, 'to finish.')
            dump(data)
        return data
