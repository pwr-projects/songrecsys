#%% 
%load_ext autoreload
%autoreload 2
from collections import Counter
from typing import List

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from gensim.models.word2vec import Word2VecKeyedVectors

from songrecsys import *

sns.set_style('white')
sns.set_context("talk", rc={'lines.linewidth': 2})
#%%
data: Data = load(DataFormat.pickle)

mgr = Manager(['spotify'], LyricsGenius, data, override=True)
pisr = PISR(mgr)
data = pisr.get_playlist_pairs()
#%%
df_data = {'epoch': [], 'track_cnt': []}
for epoch in tqdm(list(range(1, 201)), 'Gathering data'):
    model: Word2VecKeyedVectors = pisr.get_model(epochs=epoch)
    playlist = data[0]
    song: str = playlist[0]
    songs = model.most_similar(song, topn=50)
    songs_cnt = sum([pred_song[0] in playlist and pred_song[0] != song for pred_song in songs])
    # for idx, pred_song in enumerate(songs):
    #     if pred_song[0] in playlist and pred_song[0] != song:
    #         print(f'{idx}.', pred_song, 'is in playlist')
    df_data['epoch'].append(epoch)
    df_data['track_cnt'].append(songs_cnt)
df_data = pd.DataFrame.from_dict(df_data)

#%%
plot = sns.barplot(data=df_data, x='epoch', y='track_cnt')
# plot.set(yscale="log")
# plot
plot
#%%
