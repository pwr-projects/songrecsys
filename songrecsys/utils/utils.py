from pathlib import Path
from pprint import pprint
from typing import NoReturn

import numpy as np


class Summary:
    def __init__(self,
                 playlists=None,
                 tracks=None,
                 lyrics=None,
                 indent: int = 4):
        self.playlists = playlists
        self.tracks = tracks
        self.lyrics = lyrics
        self.indent = ' ' * indent

    def __call__(self):
        if self.playlists:
            self._summary_playlists()
        if self.tracks:
            self._summary_tracks()
        if self.lyrics:
            self._summary_lyrics()

    def _summary_playlists(self):
        print('Playlists:')

        count = len(self.playlists)
        avg_count_per_pl = np.round(np.average(list(map(lambda pl: len(pl.tracks),
                                                        self.playlists.values()))), 1)

        print(f'{self.indent}Count:           {count}')
        print(f'{self.indent}Avg track count: {avg_count_per_pl}')

    def _summary_tracks(self):
        print('Tracks:')

        count = len(self.tracks)

        print(f'{self.indent}Count: {count}')

    def _summary_lyrics(self):
        print('Lyrics:')

        count = len(self.lyrics)

        print(f'{self.indent}Count: {count}')


def override_prompt(default_override: bool, where: Path) -> bool:
    override = True
    if not default_override and where.exists():
        answer = input(f'{where} exists. Override? [Yy/Nn] ')
        override = answer in 'YyTt'
    return override
