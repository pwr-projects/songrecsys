from itertools import product
from multiprocessing import cpu_count
from pprint import pprint
from typing import List

from gensim.models import Word2Vec

from songrecsys.consts import DEFAULT_PATH_W2V_MODEL
from songrecsys.core.manager import Manager
from songrecsys.data import Track
from songrecsys.nlp import preprocess_title
from songrecsys.utils import tqdm


class PISR:

    def __init__(self, manager: Manager):
        self._mgr = manager
        self._data = self._mgr.data

    def _get_all_tracks_of_artist(self, artist_id: str) -> List[str]:
        artist_name = self._data.artists.get(artist_id).name
        return list(
            filter(lambda track: artist_id in self._data.tracks[track].artists_ids,
                   tqdm(self._mgr.data.tracks, f'Extracting all tracks of {artist_name}', leave=False)))

    def extract_pairs_artist_song(self, save: bool = True) -> List[str]:
        corpus: List[str] = list()
        for artist_id in tqdm(self._mgr.data.artists, 'Creating corpus', leave=False):
            artist_name = self._mgr.data.artists[artist_id].name
            tracks_titles = map(lambda track_id: preprocess_title(self._data.tracks['track_id'].title),
                                self._get_all_tracks_of_artist(artist_id))

            corpus.extend(list(product([artist_name], tracks_titles)))

        return corpus

    def get_playlist_pairs(self) -> List[str]:
        all_tracks = []
        for username in self._data.playlists:
            for playlist in tqdm(self._data.playlists.values(), f'Extracting artist-song from playlists of {username}'):
                tracks: List[Track] = list(map(self._data.tracks.get, playlist.tracks))
                for track in tracks:
                    artists_names = list(map(lambda artist_id: self._data.artists.get(artist_id).name, track.artists_ids))
                    all_tracks.append(' '.join([*artists_names, preprocess_title(track.title)]))
        return all_tracks

    def train_w2v_model(self):
        corpus = self.get_playlist_pairs()
        model = Word2Vec(corpus, iter=20, size=300, workers=cpu_count())
        model.save(DEFAULT_PATH_W2V_MODEL)
