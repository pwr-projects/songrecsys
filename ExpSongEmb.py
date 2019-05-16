#%%
# %load_ext autoreload
# %autoreload 2
import numpy as np

from songrecsys import *

#%%
data = load()
avg_playlist_length = np.average([len(pl.tracks) for pl in data.playlists.values()])
song_emb = SongEmb(data, window=15)
#%%
model = song_emb.get_model()
#%%

for playlist in data.playlists.values():
    tracks: Set[str] = playlist.tracks
    pred_songs = model.most_similar(tracks, topn=3)
    print('Acc', Meas.acc(tracks, pred_songs))
