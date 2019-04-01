import json
from pprint import pprint
from typing import Dict, Sequence

from tqdm import tqdm

from songrecsys import  ConfigMgr, SpotifyWrapper

if __name__ == '__main__':
    config = ConfigMgr()
    sp = SpotifyWrapper(config, 'spotify')
    songs = sp.pl.get_all_playlists_and_tracks()
    print(songs)
