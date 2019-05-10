import multiprocessing as mp
from itertools import chain, product
from multiprocessing import cpu_count
from pprint import pprint
from typing import List

from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec

from songrecsys.consts import FILEPATH_W2V_CORPUS, FILEPATH_W2V_MODEL
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

    def _get_all_tracks_of_artist(self, artist_id: str) -> List[str]:
        artist_name = self._data.artists[artist_id].name if artist_id in self._data.artists else None
        return list(
            filter(
                lambda track: artist_id in self._data.tracks[track].artists_ids,
                tqdm(
                    self._mgr.data.tracks,
                    f"Extracting all tracks of {artist_name}",
                    leave=False,
                ),
            ))

    def extract_pairs_artist_song(self) -> List[str]:
        corpus: List[str] = list()

        for artist_id in tqdm(self._mgr.data.artists, "Creating corpus", leave=False):
            artist_name = self._data.artists[artist_id] if artist_id in self._data.artists else None
            tracks_titles = map(
                lambda track_id: preprocess_title(self._data.tracks["track_id"].title),
                self._get_all_tracks_of_artist(artist_id),
            )

            corpus.extend(list(product([artist_name], tracks_titles)))

        with open(FILEPATH_W2V_CORPUS, 'w') as fhd:
            print('Saving corpus to', FILEPATH_W2V_CORPUS)
            fhd.writelines(corpus)

        return corpus

    def get_playlist_pairs(self) -> List[str]:
        corpus: List[str] = list()
        if FILEPATH_W2V_CORPUS.exists():
            with open(FILEPATH_W2V_CORPUS, 'r') as fhd:
                for line in fhd.readline():
                    corpus.append(line.strip())
            return corpus

        with mp.Pool(2) as pool:
            all_tracks = tqdm(pool.imap_unordered(
                mp_extract_artist_song_pair,
                [(pl, self._data.artists, self._data.tracks) for pl in self._data.playlists.values()],
            ),
                              f'Extracting artist-song from playlists',
                              total=len(self._data.playlists))
            corpus = list(chain(*all_tracks))

        with open(FILEPATH_W2V_CORPUS, 'w') as fhd:
            print('Saving corpus to', FILEPATH_W2V_CORPUS)
            fhd.writelines(map(lambda text: f'{text}\n', corpus))

        return corpus

    def train_w2v_model(self, size: int = 300, epochs: int = 20, **kwargs) -> Word2Vec:
        corpus = self.get_playlist_pairs()
        learner_info = LearnerInfo(epochs, size)
        model = Word2Vec(
            corpus,
            iter=epochs,
            size=size,
            workers=4 if cpu_count() <= 4 else cpu_count(),
            callbacks=[learner_info],
            **kwargs,
        )

        model.wv.save(str(FILEPATH_W2V_MODEL(epochs, size)))
        return model

    def get_model(self, size: int = 300, epochs: int = 20, **kwargs) -> Word2Vec:
        if FILEPATH_W2V_MODEL(epochs, size).exists():
            return Word2Vec.load(str(FILEPATH_W2V_MODEL(epochs, size)))
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

    def on_train_begin(self, model):
        print("Learning w2v model")

    def on_train_end(self, model):
        print("Learning w2v model ended")

    def on_epoch_end(self, model):
        self.epoch_bar.update()
        model.wv.save(str(FILEPATH_W2V_MODEL(self.epoch_bar.n, self.size)))

    def on_batch_end(self, model):
        self.batch_bar.update()
