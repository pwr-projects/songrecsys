from pprint import pprint
from typing import NoReturn

import numpy as np


def summary(playlists,
            tracks,
            indent: int = 2) -> NoReturn:

    info = {'playlists': len(playlists),
            'tracks': len(tracks),
            'Avg. tracks per playlist': np.round(np.average(list(map(lambda pl: len(pl.tracks),
                                                                     playlists.values()))), 1) if playlists else 0}
    max_key_length = max(map(len, info))

    print('Summary:')
    for key in info:
        spaces_after = ' ' * (max_key_length - len(key))
        print(' ' * (indent - 1), key + ':', ' ' * indent, spaces_after, info[key])
