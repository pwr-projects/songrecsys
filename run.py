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
dump(playlists, tracks, merged_data, lyrics, DataFormat.json)
# playlists, tracks = pl.get_all_playlists_and_tracks(merged_data=merged_data, update=False)

lyrics = gs.download_lyrics(tracks, lyrics)
# NLP(MAG(MAG.corpus.GOOGLE_NEWS,
#               MAG.weight.heavy,
#               300))

# NLP(MAG(MAG.corpus.COMMON_CRAWL_GL, MAG.weight.heavy, 300))
# NLP(MAG(MAG.corpus.TWITTER, MAG.weight.heavy, 200))