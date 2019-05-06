import multiprocessing as mp
from itertools import chain, product
from pprint import pprint
from sys import stdout
from time import sleep
from typing import Dict, List, NoReturn, Set

from songrecsys.config import ConfigBase
from songrecsys.data import dump
from songrecsys.schemes import Album, Artist, Data, Track
from songrecsys.spotify import PlaylistMgr, SpotifyWrapper
from songrecsys.utils import tqdm


def mp_artist_extractor(args) -> Artist:
    sp, artist_id = args
    # stdout.write(f'Downloading artist: {artist_id}\n')
    # stdout.flush()
    not_downloaded = True
    while not_downloaded:
        try:
            artist = ArtistsDownloader.extra_info_from_artist(sp, artist_id)
            not_downloaded = False
        except:
            # stdout.write(f'Retrying to download artist: {artist_id}\n')
            # stdout.flush()
            sleep(2)
    return artist


class ArtistsDownloader:

    def __init__(self, sp: SpotifyWrapper, config: ConfigBase, data: Data):
        self._data: Data = data
        self._sp: SpotifyWrapper = sp
        self._config: ConfigBase = config

    def extract_all_artists_from_data(self) -> Set[str]:
        artists: set = set()

        for track in tqdm(self._data.tracks.values(), 'Extracting artists'):
            if hasattr(track, 'artists_ids'):
                artists.update(set(track.artists_ids))
        return artists

    def _extract_info_from_artist(self, artist_id: str) -> Artist:
        return self.extra_info_from_artist(self._sp, artist_id)

    @classmethod
    def extra_info_from_artist(cls, sp: SpotifyWrapper, artist_id: str) -> Artist:
        artist_info = sp.artist(artist_id)
        return Artist.from_api(artist_info)

    def get_albums_of_artist(self, artists_id: str) -> List[Album]:
        all_albums: list = list()

        albums = self._sp.artist_albums(artists_id, album_type='album', limit=50)

        while albums:
            all_albums.extend(albums['items'])
            sleep(self._config.request_interval)
            albums = self._sp.next(albums) if albums['next'] else None

        all_albums = list(map(Album.from_api, all_albums))
        return all_albums

    def add_albums_to_data(self, albums: List[Album]) -> NoReturn:
        for album in albums:
            if album.id not in self._data.albums.keys():
                self._data.albums[album.id] = Album(**album.__dict__, use_id=False)

    def get_all_tracks_from_album(self, album_id: str) -> List[Track]:
        all_tracks: list = list()
        tracks = self._sp.album_tracks(album_id)
        while tracks:
            all_tracks.extend(tracks['items'])
            sleep(self._config.request_interval)
            tracks = self._sp.next(tracks) if tracks['next'] else None

        return list(map(Track.from_api, all_tracks))

    def get_all_albums_and_all_tracks(self, save_interval: int = 20, only_playlists: bool = True) -> Data:
        if only_playlists:
            artist_ids: set = set()
            for pl in self._data.playlists.values():
                for track in pl.tracks:
                    artist_ids.update(set(self._data.tracks[track].artists_ids))
        else:
            artist_ids = self.extract_all_artists_from_data()

        artists_loop_str = 'Downloading albums of artist'
        albums_loop_str = 'Downloading tracks of album'

        # with mp.Pool(1) as pool:
        #     for artist in tqdm(pool.imap_unordered(mp_artist_extractor, list(product([self._sp], artist_ids))),
        #                        'Downloading artist info',
        #                        total=len(artist_ids)):
        #         artist.add_to_data(self._data)

        with tqdm(artist_ids, artists_loop_str) as artist_bar:
            for artist_id in artist_bar:
                if artist_id not in self._data.artists:
                    artist = mp_artist_extractor((self._sp, artist_id))
                    artist_bar.set_description(f'{artists_loop_str} - {artist.name}')
                    artist.add_to_data(self._data)


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
        return self._data
