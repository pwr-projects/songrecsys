#!.env/bin/python
from pprint import pprint

from songrecsys import *

if __name__ == '__main__':
    data:Data = load(DataFormat.pickle)

    mgr = Manager(['spotify'], LyricsGenius, data, override=True)


    # mgr.pl.download_data()
    # mgr.lp.download_lyrics(data)
    Summary.show(data, 4)
    
    # mgr.ad.get_all_albums_and_all_tracks(save_interval=50, only_playlists=True)
    # Summary.show(data, 4)



    # nlp = NLP(MAG(MAG.corpus.GOOGLE_NEWS, MAG.weight.heavy, 300))
    pisr = PISR(mgr)
    pisr.train_w2v_model(epochs=200)
