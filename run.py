#!.env/bin/python
from pprint import pprint
from typing import Dict, Sequence

from tqdm import tqdm

from songrecsys import *

if __name__ == '__main__':
    config = ConfigMgr()
    # sp = SpotifyWrapper(config, 'spotify')

    # pl = PlaylistMgr(sp)
    # songs = pl.get_all_playlists_and_tracks(save=True, load_saved=True, max_playlist_count=1)
    # pl.summary(songs)

    # gs = LyricsGenius(config)
    # songs = gs.add_lyrics_to_dataset(songs)

    NLP(MAG.get(MAG.corpus.WIKIPEDIA, MAG.weight.medium, 300))
