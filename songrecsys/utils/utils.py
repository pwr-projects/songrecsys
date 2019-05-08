from itertools import zip_longest
from pathlib import Path
from typing import NoReturn

import numpy as np
from tqdm.autonotebook import tqdm as tdqm_orig

from songrecsys.schemes import Data


class Summary:

    DEFAULT_INDENT = 4

    def __init__(self, indent: int = DEFAULT_INDENT):
        self._indent = self.indent(indent)

    def __call__(self, data: Data, indent: int = DEFAULT_INDENT) -> NoReturn:
        self.show(data, self._indent)

    @classmethod
    def indent(cls, indent: int) -> str:
        return ' ' * indent

    @classmethod
    def show(cls, data: Data, indent: int = DEFAULT_INDENT) -> NoReturn:
        if data.playlists:
            cls._summary_playlists(data, indent)
        if data.tracks:
            cls._summary_tracks(data, indent)
        if data.artists:
            cls._summary_artists(data, indent)

    @classmethod
    def _summary_playlists(cls, data: Data, indent: int) -> NoReturn:
        _indent = cls.indent(indent)

        print('Playlists:')

        count = len(data.playlists)
        avg_count_per_pl = [
            len(data.playlists[pl].tracks)
            for pl in tqdm(data.playlists, 'Summary: filtering playlists', leave=False)
            if data.playlists[pl].tracks
        ]
        avg_count_per_pl = np.average(avg_count_per_pl)
        avg_count_per_pl = np.round(avg_count_per_pl, 1)

        print(f'{_indent}Count:             {count}')
        print(f'{_indent}Avg track count:   {avg_count_per_pl}')

    @classmethod
    def _summary_tracks(cls, data: Data, indent: int) -> NoReturn:
        _indent = cls.indent(indent)

        print('Tracks:')

        count = len(data.tracks)
        count_with_lyrics = sum(
            map(lambda track: int(bool(track.lyrics)),
                tqdm(data.tracks.values(), 'Summary: filtering tracks w/out lyrics', leave=False)))

        print(f'{_indent}Count:             {count}')
        print(f'{_indent}Count with lyrics: {count_with_lyrics}')

    @classmethod
    def _summary_artists(cls, data: Data, indent: int) -> NoReturn:
        _indent = cls.indent(indent)

        print('Artists:')

        count = len(data.artists)

        print(f'{_indent}Count:             {count}')


def override_prompt(default_override: bool, where: Path) -> bool:
    override = True
    if not default_override and where.exists():
        answer = input(f'{where} exists. Override? [Yy/Nn] ')
        override = answer in 'YyTt'
    return override


def tqdm(*args, **kwargs):
    return tdqm_orig(*args, **kwargs, dynamic_ncols=True, miniters=1, mininterval=0.1)
    # return tdqm_orig(*args, **kwargs)


def grouper(iterable, n: int, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)
