#!.env/bin/python
import csv
from pprint import pprint
from typing import Dict, Sequence

from songrecsys import *

if __name__ == '__main__':
    config = ConfigMgr()
    sp = SpotifyWrapper(config, 'spotify')
    gs = LyricsGenius(config)
    pl = PlaylistMgr(sp)

    playlists, tracks = pl.get_all_playlists_and_tracks(load_saved=True, update=False)
    summary(playlists, tracks)
    playlists = gs.add_lyrics_to_dataset(tracks)

    # nlp = NLP(MAG(MAG.corpus.GOOGLE_NEWS,
    #               MAG.weight.medium,
    #               300), force_download=True)

    # for key, vector in nlp():
    #     print(key, end=' ')
