#!.env/bin/python
from songrecsys import *

if __name__ == '__main__':
    data = load(DataFormat.pickle)
    mgr = Manager(['spotify'], LyricsGenius, data)


    Summary.show(data, 4)
    mgr.pl.download_data(update=False)
    dump(data, DataFormat.json)
    lyrics = mgr.lp.download_lyrics(data)
    dump(data, DataFormat.json)
    # nlp = NLP(MAG(MAG.corpus.GOOGLE_NEWS, MAG.weight.heavy, 300))
