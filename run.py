#!.env/bin/python
from songrecsys import *

if __name__ == '__main__':
    data = load(DataFormat.pickle)
    # # CLEAN DATA
    # for track in list(data.tracks.keys()):
    #     if not data.tracks[track].check():
    #         del data.tracks[track]
    # for artist in list(data.artists.keys()):
    #     if not data.artists[artist].check():
    #         del data.artists[artist]
    # for album in list(data.albums.keys()):
    #     if not data.album[album].check():
    #         del data.albums[album]
    mgr = Manager(['spotify'], LyricsGenius, data, override=True)

    Summary.show(data, 4)
    # mgr.pl.download_data()
    # dump(data, DataFormat.json)

    # mgr.lp.download_lyrics(data)
    # dump(data, DataFormat.json)

    mgr.ad.get_all_albums_and_all_tracks(save_interval=50, only_playlists=True)
    dump(data)
    # nlp = NLP(MAG(MAG.corpus.GOOGLE_NEWS, MAG.weight.heavy, 300))
    pisr = PISR(mgr)
    pisr.train_w2v_model()