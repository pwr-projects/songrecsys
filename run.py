#!.env/bin/python
#%%
from songrecsys import *
from songrecsys.utils.utils import tqdm

config = ConfigMgr()
sp = SpotifyWrapper(config, 'spotify')
gs = LyricsGenius(config)
lw = LyricWikia(config)
pl = PlaylistMgr(sp)

loaded_data = load(playlists=True, tracks=True, lyrics=True, merged_data=True, data_format=DataFormat.pickle)
playlists, tracks, merged_data, lyrics = tuple(map(loaded_data.get, ['playlists',
                                                                     'tracks',
                                                                     'merged_data',
                                                                     'lyrics']))

Summary(playlists=playlists, tracks=tracks, lyrics=lyrics)()

# playlists, tracks = pl.get_all_playlists_and_tracks(merged_data=merged_data, update=False)

lyrics = gs.download_lyrics(tracks, lyrics)
NLP(MAG(MAG.corpus.GOOGLE_NEWS,
              MAG.weight.heavy,
              300))

NLP(MAG(MAG.corpus.COMMON_CRAWL_GL, MAG.weight.heavy, 300))
NLP(MAG(MAG.corpus.TWITTER, MAG.weight.heavy, 200))

# for key, vector in nlp():
#     print(key, end=' ')

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
