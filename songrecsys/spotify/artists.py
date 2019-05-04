from pprint import pprint
from time import sleep
from typing import Dict, List, NoReturn, Set

from songrecsys.data import dump
from songrecsys.schemes import Album, Artist, Data, Track
from songrecsys.spotify import PlaylistMgr, SpotifyWrapper
from songrecsys.utils import tqdm


class ArtistsDownloader:

    def __init__(self, sp: SpotifyWrapper, data: Data):
        self._data: Data = data
        self._sp: SpotifyWrapper = sp

    def extract_all_artists_from_data(self) -> Set[str]:
        artists: set = set()

        for track in tqdm(self._data.tracks.values(), 'Extracting artists'):
            if hasattr(track, 'artists_ids'):
                artists.update(set(track.artists_ids))
        return artists

    def extract_info_from_artist(self, artist_id: str) -> Artist:
        artist_info = self._sp.artist(artist_id)
        return Artist(**artist_info)

    def add_artist_to_data(self, artist: Artist) -> NoReturn:
        if artist.id not in self._data.artists:
            self._data.artists[artist.id] = Artist(**artist.__dict__, use_id=False)

    def extract_info_from_album(self, album: dict) -> Album:
        artists_id = set(map(lambda artist: artist['id'], album['artists']))
        return Album(artists_id=artists_id, **album)

    def get_albums_of_artist(self, artists_id: str) -> List[Album]:
        if hasattr(self._data.artists.get(artists_id), 'albums_downloaded') and hasattr(
                self._data.artists.get(artists_id), 'albums_id'):
            return self._data.artists.get(artists_id).albums_id
        all_albums: list = list()
        albums = self._sp.artist_albums(artists_id, limit=50)

        while albums:
            all_albums.extend(albums['items'])
            albums = self._sp.next(albums) if albums['next'] else None

        all_albums = list(map(self.extract_info_from_album, all_albums))
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
            tracks = self._sp.next(tracks) if tracks['next'] else None

        return list(map(PlaylistMgr.extract_specific_info_from_track_item, all_tracks))

    def get_all_albums_and_all_tracks(self) -> Data:
        artist_ids = self.extract_all_artists_from_data()

        artists_loop_str = 'Downloading albums of artist'
        albums_loop_str = 'Downloading tracks of album'
        with tqdm(artist_ids, artists_loop_str) as artist_bar:
            for artist_id in artist_bar:
                sleep(1)
                artist = self.extract_info_from_artist(artist_id)
                self.add_artist_to_data(artist)
                artist_bar.set_description(f'{artists_loop_str} - {artist.name}')

                albums = self.get_albums_of_artist(artist_id)
                self.add_albums_to_data(albums)

                with tqdm(albums, albums_loop_str) as album_bar:
                    try:
                        for album in album_bar:
                            album_bar.set_description(f'{albums_loop_str}')
                            if not hasattr(album, 'tracks') or (hasattr(album, 'tracks') and not album.tracks):
                                album_bar.set_description(f'{albums_loop_str} - {album.id}')
                                sleep(0.2)
                                tracks = self.get_all_tracks_from_album(album.id)
                                album.tracks = list(map(lambda tr: tr.id, tracks))
                                album.songs_downloaded = True
                                for track in tracks:
                                    track.add_to_data(self._data)
                        dump(self._data, verbose=False)
                    except Exception as e:
                        print(e)
        return self._data
