from pathlib import Path
from typing import NoReturn

import numpy as np
from tqdm.auto import tqdm as tdqm_orig

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

    @classmethod
    def _summary_playlists(cls, data: Data, indent: int) -> NoReturn:
        indent = cls.indent(indent)

        for username in data.playlists:
            print(f'Playlists of user: {username}')

            count = len(data.playlists.get(username))
            avg_count_per_pl = map(lambda pl: len(pl.tracks), data.playlists.get(username))
            avg_count_per_pl = np.average(list(avg_count_per_pl))
            avg_count_per_pl = np.round(avg_count_per_pl, 1)

            print(f'{indent}Count:           {count}')
            print(f'{indent}Avg track count: {avg_count_per_pl}')

    @classmethod
    def _summary_tracks(cls, data: Data, indent: int) -> NoReturn:
        indent = cls.indent(indent)

        print('Tracks:')

        count = len(data.tracks)
        count_with_lyrics = sum(map(lambda track: int(bool(track.lyrics)), data.tracks.values()))

        print(f'{indent}Count:             {count}')
        print(f'{indent}Count with lyrics: {count_with_lyrics}')


def override_prompt(default_override: bool, where: Path) -> bool:
    override = True
    if not default_override and where.exists():
        answer = input(f'{where} exists. Override? [Yy/Nn] ')
        override = answer in 'YyTt'
    return override


def tqdm(*args, **kwargs):
    return tdqm_orig(*args, **kwargs, miniters=1, mininterval=0.1)
    # return tdqm_orig(*args, **kwargs)
