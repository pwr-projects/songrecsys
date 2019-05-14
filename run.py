#!.env/bin/python
from pprint import pprint

from songrecsys import *

if __name__ == '__main__':
    data = load(DataFormat.pickle)
    Summary.show(data, 4)

    mgr = Manager(['spotify'], LyricsGenius, data)

    # # GET NEW DATA
    # mgr.pl.download_data()
    # mgr.lp.download_lyrics(data)
    mgr.pl.download_all_audio_features()
    Summary.show(data, 4)

    # mgr.ad.get_all_albums_and_all_tracks(save_interval=50, only_playlists=False)
    # Summary.show(data, 4)

    # pisr = PISR(mgr)
    # pisr.train_w2v_model(epochs=200)

    # nlp = NLP(MAG(MAG.corpus.GOOGLE_NEWS, MAG.weight.heavy, 300))