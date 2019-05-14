import multiprocessing as mp
from itertools import chain, groupby, product
from multiprocessing import cpu_count
from operator import not_
from pprint import pprint
from typing import Iterable, List

from gensim.models import KeyedVectors, Word2Vec
from gensim.models.callbacks import CallbackAny2Vec
from gensim.utils import RULE_KEEP

from songrecsys.consts import *
from songrecsys.core.manager import *
from songrecsys.data import *
from songrecsys.misc import *
from songrecsys.multiprocessing import *
from songrecsys.nlp import *
from songrecsys.schemes import *

__all__ = ['PISR']


class PISR:

    def __init__(self, manager):
        self._mgr = manager
        self._data = self._mgr.data
        self._model = None

    def get_playlist_pairs(self):
        corpus = list()

        split_playlists = lambda tracks: [list(group) for k, group in groupby(tracks, bool) if k]

        if FILEPATH_PISR_CORPUS.exists():
            print(f'Loading corpus from {FILEPATH_PISR_CORPUS}')
            with open(FILEPATH_PISR_CORPUS, 'r') as fhd:
                return split_playlists([txt.strip() for txt in fhd.readlines()])

        for playlist in tqdm(self._data.playlists.values(), 'Corpus: playlist'):
            all_tracks = list()
            tracks = [self._data.tracks[tr] for tr in playlist.tracks if tr in self._data.tracks]
            for track in tqdm(tracks, 'Corpus: track', leave=False):
                artists_names = [
                    self._data.artists[artist_id].name.lower()
                    for artist_id in track.artists_ids
                    if self._data.artists.get(artist_id)
                ]
                # all_tracks.append(" ".join([*artists_names, preprocess_title(track.title.lower())]))
                all_tracks.append(preprocess_title(track.title.lower()))
            all_tracks.append(' ')
            corpus.append(all_tracks)

        with open(FILEPATH_PISR_CORPUS, 'w') as fhd:
            print('Saving corpus to', FILEPATH_PISR_CORPUS)
            fhd.writelines([f'{text}\n' for text in chain(*corpus)])

        return split_playlists(chain(*corpus))

    def train_w2v_model(self, corpus=None, path=FILEPATH_PISR_W2V_MODEL, size=300, epochs=20, **kwargs):
        corpus = corpus if corpus else self.get_playlist_pairs()
        learner_info = LearnerInfo(epochs, size)

        model = Word2Vec(window=10, size=size, workers=cpu_count())
        model.build_vocab(corpus, trim_rule=lambda *_: RULE_KEEP)
        model.train(corpus, epochs=epochs, total_words=len(list(chain(*corpus))), callbacks=[learner_info])

        model.wv.save(str(path(epochs, size)))
        return model

    def get_model(self, size=300, epochs=20, **kwargs):
        if FILEPATH_PISR_W2V_MODEL(epochs, size).exists():
            return KeyedVectors.load(str(FILEPATH_PISR_W2V_MODEL(epochs, size)))
        return self.train_w2v_model(size, epochs, **kwargs)

    def evaluate(self):
        if self._model:
            corpus = self.get_playlist_pairs()
            score = self._model.score(corpus[:1000000], total_sentences=1000000)
            print(score)


class LearnerInfo(CallbackAny2Vec):

    def __init__(self, epochs, size):
        self.epoch_bar = tqdm(desc="Epochs", total=epochs)
        self.batch_bar = tqdm(desc='Batch')
        self.size = size

    def on_epoch_end(self, model):
        self.epoch_bar.update()
        model.wv.save(str(FILEPATH_PISR_W2V_MODEL(self.epoch_bar.n, self.size)))

    def on_batch_end(self, model):
        self.batch_bar.update()
