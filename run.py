#!.env/bin/python
from pprint import pprint
from typing import Dict, Sequence

from tqdm import tqdm

from songrecsys import *

if __name__ == '__main__':
    config = ConfigMgr()
    sp = SpotifyWrapper(config, 'spotify')
    gs = LyricsGenius(config)
    pl = PlaylistMgr(sp)

    playlists, tracks = pl.get_all_playlists_and_tracks(load_saved=True, update=False)
    summary(playlists, tracks)
    playlists = gs.add_lyrics_to_dataset(tracks)

    # nlp = NLP(MAG.get(MAG.corpus.WIKIPEDIA, MAG.weight.heavy, 300))

    # for key, vector in nlp():
    #     print(key, end=' ')
