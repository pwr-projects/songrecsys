from pprint import pprint

from songrecsys import *
from tqdm import tqdm
import json
from typing import Sequence, Dict

if __name__ == '__main__':
    config = ConfigMgr(CONFIG_DEFAULT_PATH)
    sp = SpotifyWrapper(config, 'spotify')

    playlist_ids = sp.get_all_playlists_of_user()
    songs = sp.get_tracks_from_playlists(*playlist_ids)

    with open('songs.json', 'w') as fhd:
        json.dump(songs, fhd, indent=4)

