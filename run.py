#!.env/bin/python
from songrecsys import *

if __name__ == '__main__':

    mgr = Manager(['spotify'], LyricsGenius)

    data = load(DataFormat.pickle)
    dump(data, DataFormat.json)
    # print(data)

    Summary.show(data, 4)
    # playlists, tracks = mgr.pl.get_all_playlists_and_tracks_of_user(merged_data=data.merged_data, update=False)
    # lyrics = mgr.lp.download_lyrics(data.tracks, data.lyrics)

    # nlp = NLP(MAG(MAG.corpus.GOOGLE_NEWS, MAG.weight.heavy, 300))
