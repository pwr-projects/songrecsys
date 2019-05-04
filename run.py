#!.env/bin/python
from songrecsys import *

if __name__ == '__main__':
    data = load(DataFormat.pickle)
    data = Data(data.playlists, data.tracks)
    mgr = Manager(['spotify'], LyricsGenius, data)

    Summary.show(data, 4)
    # mgr.pl.download_data()
    dump(data, DataFormat.json)

    # mgr.lp.download_lyrics(data)
    # dump(data, DataFormat.json)

    mgr.ad.get_all_albums_and_all_tracks()
    dump(data)
    # nlp = NLP(MAG(MAG.corpus.GOOGLE_NEWS, MAG.weight.heavy, 300))
