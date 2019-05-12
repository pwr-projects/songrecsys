import re
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import *

from songrecsys.nlp import preprocess_title

__all__ = ['AudioFeatures', 'Data', 'Artist', 'Album', 'Playlist', 'Track']


class BaseDataItem(ABC):

    def checkattr(self, name: str = 'id'):
        if not hasattr(self, name):
            raise Exception(f'Cannot add to data because there is no `{name}` attribute')

    @abstractmethod
    def add_to_data(self, data, override):
        raise NotImplementedError

    @abstractmethod
    def check(self) -> bool:
        raise NotImplementedError


class AudioFeatures(BaseDataItem):

    def __init__(self,
                 id: str,
                 danceability: float,
                 energy: float,
                 key: int,
                 loudness: float,
                 mode: int,
                 speechiness: float,
                 acousticness: float,
                 instrumentalness: float,
                 liveness: float,
                 valence: float,
                 tempo: float,
                 duration_ms: int,
                 time_signature: int,
                 use_id: bool = True,
                 **_):
        self.danceability = danceability
        self.energy = energy
        self.key = key
        self.loudness = loudness
        self.mode = mode
        self.speechiness = speechiness
        self.acousticness = acousticness
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.valence = valence
        self.tempo = tempo
        self.duration_ms = duration_ms
        self.time_signature = time_signature
        if use_id:
            self.id = id

    def add_to_data(self, data, override: bool = True):
        self.checkattr()
        if override or not data.tracks[self.id].audio_features:
            data.tracks[self.id].audio_features = AudioFeatures(**self.__dict__, use_id=False)

    @classmethod
    def from_api(cls, audio_features_item: dict):
        return AudioFeatures(**audio_features_item)

    def check(self) -> bool:
        return False

    def to_list(self) -> Iterable[Union[float, int]]:
        return [
            getattr(self, atr) for atr in [
                'danceability',
                'energy',
                'key',
                'loudness',
                'mode',
                'speechiness',
                'acousticness',
                'instrumentalness',
                'liveness',
                'valence',
                'tempo',
                'duration_ms',
                'time_signature',
            ]
        ]


class Track(BaseDataItem):

    def __init__(self,
                 title: str = None,
                 artists_ids: Set[str] = None,
                 lyrics: str = None,
                 audio_features: AudioFeatures = None,
                 id: str = None,
                 use_id: bool = True,
                 **_):
        self.title = preprocess_title(title)
        self.artists_ids = artists_ids if artists_ids else set()
        self.lyrics = lyrics
        self.audio_features = audio_features
        if use_id:
            self.id = id

    def add_to_data(self, data, override: bool = True):
        self.checkattr()
        if override or self.id not in data.tracks:
            data.tracks[self.id] = Track(**self.__dict__, use_id=False)
        return data

    def check(self) -> bool:
        return all(map(lambda attr: hasattr(self, attr),
                       ['title', 'lyrics', 'artists_ids'])) and not hasattr(self, 'id')

    @classmethod
    def from_api(cls, track_item: dict):
        artists_ids = list(map(lambda artist_info: artist_info['id'], track_item['artists']))
        title = track_item['name']
        del track_item['artists']
        return Track(title, artists_ids, **track_item)


class Playlist(BaseDataItem):

    def __init__(self,
                 username: str = None,
                 id: str = None,
                 name: str = None,
                 tracks: Set[str] = None,
                 use_id: bool = True,
                 **_):
        self.username = username
        if use_id:
            self.id: str = id
        self.name: str = name
        self.tracks: Set[str] = tracks if tracks else set()

    def add_to_data(self, data, override: bool = True):
        self.checkattr()
        if override or self.id not in data.playlists:
            data.playlists[self.id] = Playlist(**self.__dict__, use_id=False)
        return data

    def check(self) -> bool:
        return all(map(lambda attr: hasattr(self, attr), ['username', 'name', 'tracks'])) and not hasattr(self, 'id')

    @classmethod
    def from_api(self, playlist_item: dict):
        username = playlist_item['owner']['id']
        del playlist_item['tracks']
        return Playlist(username, **playlist_item)


class Artist(BaseDataItem):

    def __init__(self, name: str, albums_id: Set[str] = None, id: str = None, use_id: bool = True, **_):
        self.name = name
        self.albums_id = albums_id if albums_id else set()
        if use_id:
            self.id = id

    def add_to_data(self, data, override: bool = True):
        self.checkattr()
        if override or self.id not in data.artists:
            data.artists[self.id] = Artist(**self.__dict__, use_id=False)
        return data

    def check(self) -> bool:
        return all(map(lambda attr: hasattr(self, attr), ['name', 'albums_id'])) and not hasattr(self, 'id')

    @classmethod
    def from_api(self, artist_item: dict):
        return Artist(**artist_item)

    @classmethod
    def download_info_about_artist(cls, sp, artist_id: str):
        artist_info = sp.artist(artist_id)
        return Artist.from_api(artist_info)


class Album(BaseDataItem):

    def __init__(self,
                 id: str = None,
                 artists_id: Set[str] = None,
                 tracks: Set[str] = None,
                 name: str = None,
                 use_id: bool = True,
                 **_):
        if use_id:
            self.id = id
        self.artists_id = artists_id if artists_id else set()
        self.name = name
        self.tracks = tracks if tracks else set()

    def add_to_data(self, data, override):
        self.checkattr()
        if override or self.id not in data.albums:
            data.albums[self.id] = Album(**self.__dict__, use_id=False)
        return data

    def check(self) -> bool:
        return all(map(lambda attr: hasattr(self, attr), ['artists_id', 'name'])) and not hasattr(self, 'id')

    @classmethod
    def from_api(self, album_item: dict):
        artists_id = set(map(lambda artist: artist['id'], album_item['artists']))
        return Album(artists_id=artists_id, **album_item)


class Data:

    def __init__(self, playlists: dict = None, tracks: dict = None, artists: dict = None, albums: dict = None, **_):
        self.playlists = playlists if playlists else defaultdict(Playlist)
        self.tracks = tracks if tracks else defaultdict(Track)
        self.artists = artists if artists else defaultdict(Artist)
        self.albums = albums if albums else defaultdict(Album)

    @classmethod
    def from_json(cls, data: dict):
        _data = {k: data[k] for k in ['playlists', 'tracks', 'artists', 'albums'] if data.get(k)}
        return Data(**_data)
