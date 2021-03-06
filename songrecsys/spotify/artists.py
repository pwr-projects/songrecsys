import multiprocessing as mp
from itertools import chain, product
from pprint import pprint
from sys import stdout
from time import sleep
from typing import *

from songrecsys.config import *
from songrecsys.data_manager import *
from songrecsys.misc import *
from songrecsys.multiprocessing import *
from songrecsys.schemes import *
from songrecsys.spotify.playlist_mgr import *
from songrecsys.spotify.spotify_wrapper import *

__all__ = ['ArtistsDownloader']


class ArtistsDownloader:

    def __init__(self, sp: SpotifyWrapper, config: ConfigBase, data: Data):
        self._data = data
        self._sp = sp
        self._config = config

    def extract_all_artists_from_data(self) -> Set[str]:
        artists: Set[str] = set()

        for track in tqdm(self._data.tracks.values(), 'Extracting artists'):
            artists.update(track.artists_ids)
        return artists

    def _download_info_about_artist(self, artist_id: str) -> Artist:
        return Artist.download_info_about_artist(self._sp, artist_id)

    def get_albums_of_artist(self, artists_id: Set[str]) -> Iterable[Album]:
        all_albums: List[Album] = []

        albums = self._sp.artist_albums(artists_id, album_type='album', limit=50)

        while albums:
            all_albums.extend(map(Album.from_api, albums['items']))
            sleep(getattr(self._config, 'request_interval', 0.1))
            albums = self._sp.next(albums) if albums['next'] else None

        return all_albums

    def add_albums_to_data(self, albums: List[Dict[str, Any]]) -> Data:
        for album in albums:
            Album.from_api(album).add_to_data(self._data)
        return self._data

    def get_all_tracks_from_album(self, album_id: str) -> Iterable[Track]:
        all_tracks: List[Track] = []
        tracks = self._sp.album_tracks(album_id)
        while tracks:
            all_tracks.extend(map(Track.from_api, tracks['items']))
            sleep(getattr(self._config, 'request_interval', 0.1))
            tracks = self._sp.next(tracks) if tracks['next'] else None
        return all_tracks

    def get_all_albums_and_all_tracks(self, save_interval: int = 50, only_playlists: bool = True) -> Data:
        if only_playlists:
            artist_ids = set()
            for pl in tqdm(self._data.playlists.values()):
                for track in tqdm(pl.tracks):
                    artist_ids.update(set(self._data.tracks[track].artists_ids))
            artist_ids = {art for art in artist_ids if art in self._data.artists}
        else:
            artist_ids = self.extract_all_artists_from_data()

        artists_loop_str = 'Downloading artists info'
        albums_loop_str = 'Downloading albums of artist'
        tracks_loop_str = 'Downloading tracks of album'

        # with mp.Pool(3) as pool:
        #     for artist in tqdm(pool.imap_unordered(mp_artist_extractor, product([self._sp], artist_ids)),
        #                        'Downloading artist info',
        #                        total=len(artist_ids)):
        #         artist.add_to_data(self._data)

        with tqdm(list(enumerate(artist_ids)), artists_loop_str) as artist_bar:
            for save_interval_cnt, artist_id in artist_bar:
                if artist_id and artist_id not in self._data.artists:
                    artist = mp_artist_extractor((self._sp, artist_id))
                    artist_bar.set_description(f'{artists_loop_str} - {artist.name}')
                    artist.add_to_data(self._data)
                if save_interval_cnt % save_interval == 0:
                    artist_bar.set_description(f'{artists_loop_str} - saving')
                    dump(self._data, verbose=False)

        # albums = self.get_albums_of_artist(artist_id)

        # self.add_albums_to_data(albums)

        # with tqdm(albums, albums_loop_str, leave=False) as album_bar:
        #     for album in album_bar:
        #         try:
        #             album_bar.set_description(f'{albums_loop_str}')

        #             if not hasattr(album, 'tracks') or (hasattr(album, 'tracks') and not album.tracks):
        #                 album_bar.set_description(f'{albums_loop_str} - {album.name}')

        #                 tracks = self.get_all_tracks_from_album(album.id)
        #                 album.tracks = list(map(lambda tr: tr.id, tracks))

        #                 for track in tracks:
        #                     track.add_to_data(self._data)
        #         except Exception as e:
        #             print(e)

        # if save_interval_cnt % save_interval == 0:
        #     artist_bar.set_description(f'{artists_loop_str} - saving')
        #     dump(self._data, verbose=False)
        return dump(self._data)
