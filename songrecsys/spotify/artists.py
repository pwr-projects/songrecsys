from typing import Set

from songrecsys.schemes import Data
from songrecsys.spotify import SpotifyWrapper
from songrecsys.utils import tqdm


class ArtistsDownloader:

    def __init__(self, sp: SpotifyWrapper, data: Data):
        self._data: Data = data
        self._sp: SpotifyWrapper = sp

    def extract_all_artists(self) -> Set[str]:
        artists: set = set()
        for track in tqdm(self._data.tracks.values(), 'Extracting artists'):
            artists.update(set(track.artists_ids))

    def get_songs_of_artist(self):
        