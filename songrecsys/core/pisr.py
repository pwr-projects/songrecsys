import multiprocessing as mp
from itertools import chain, groupby, product
from multiprocessing import cpu_count
from operator import not_
from pprint import pprint
from typing import List

from gensim.models import KeyedVectors, Word2Vec
from gensim.models.callbacks import CallbackAny2Vec
from gensim.utils import RULE_KEEP

from songrecsys.consts import DEFAULT_PATH_CORPUS, DEFAULT_PATH_W2V_MODEL
from songrecsys.core.manager import Manager
from songrecsys.data import Data, Track
from songrecsys.multiprocessing import mp_extract_artist_song_pair
from songrecsys.nlp import preprocess_title
from songrecsys.utils import tqdm


class PISR:

    def __init__(self, manager: Manager):
        self._mgr: Manager = manager
        self._data: Data = self._mgr.data
        self._model: Word2Vec = None

    def get_playlist_pairs(self) -> List[List[str]]:
        corpus: List[List[str]] = list()

        split_playlists = lambda tracks: [list(group) for k, group in groupby(tracks, bool) if k]

        if DEFAULT_PATH_CORPUS.exists():
            print(f'Loading corpus from {DEFAULT_PATH_CORPUS}')
            with open(DEFAULT_PATH_CORPUS, 'r') as fhd:
                return split_playlists(map(lambda txt: txt.strip(), fhd.readlines()))

        # with mp.Pool(2) as pool:
        #     all_tracks = tqdm(pool.imap_unordered(
        #         mp_extract_artist_song_pair,
        #         [(pl, self._data.artists, self._data.tracks) for pl in self._data.playlists.values()],
        #     ),
        #                       f'Extracting artist-song from playlists',
        #                       total=len(self._data.playlists))
        #     corpus = list(chain(*all_tracks))

        for playlist in tqdm(self._data.playlists.values(), 'Corpus: playlist'):
            all_tracks: List[str] = list()
            tracks: List[Track] = [self._data.tracks[tr] for tr in playlist.tracks if tr in self._data.tracks]
            for track in tqdm(tracks, 'Corpus: track', leave=False):
                artists_names: list = [
                    self._data.artists[artist_id].name.lower()
                    for artist_id in track.artists_ids
                    if self._data.artists.get(artist_id)
                ]
                # all_tracks.append(" ".join([*artists_names, preprocess_title(track.title.lower())]))
                all_tracks.append(preprocess_title(track.title.lower()))
            all_tracks.append(' ')
            corpus.append(all_tracks)

        with open(DEFAULT_PATH_CORPUS, 'w') as fhd:
            print('Saving corpus to', DEFAULT_PATH_CORPUS)
            fhd.writelines(map(lambda text: f'{text}\n', chain(*corpus)))

        return split_playlists(chain(*corpus))

    def train_w2v_model(self, corpus=None, path=DEFAULT_PATH_W2V_MODEL, size: int = 300, epochs: int = 20, **kwargs) -> Word2Vec:
        corpus = corpus if corpus else self.get_playlist_pairs()
        learner_info = LearnerInfo(epochs, size)

        model = Word2Vec(window=10, size=size, workers=cpu_count())
        model.build_vocab(corpus, trim_rule=lambda a, b, c: RULE_KEEP)
        model.train(corpus, epochs=epochs, total_words=len(list(chain(*corpus))), callbacks=[learner_info])

        model.wv.save(str(path(epochs, size)))
        return model

    def get_model(self, size: int = 300, epochs: int = 20, **kwargs) -> Word2Vec:
        if DEFAULT_PATH_W2V_MODEL(epochs, size).exists():
            return KeyedVectors.load(str(DEFAULT_PATH_W2V_MODEL(epochs, size)))
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
        self.size: int = size

    def on_epoch_end(self, model):
        self.epoch_bar.update()
        model.wv.save(str(DEFAULT_PATH_W2V_MODEL(self.epoch_bar.n, self.size)))

    def on_batch_end(self, model):
        self.batch_bar.update()
