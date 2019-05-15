from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import *

import pandas as pd

from songrecsys.nlp import *

__all__ = ['AudioFeatures', 'Data', 'Artist', 'Album', 'Playlist', 'Track']


class BaseDataItem:

    def checkattr(self, name: str = 'id'):
        if not hasattr(self, name):
            raise Exception(f'Cannot add to data because there is no `{name}` attribute')

    @abstractmethod
    def add_to_data(self, data: Data) -> Data:
        raise NotImplementedError

    @abstractmethod
    def check(self) -> bool:
        raise NotImplementedError

    def use_id(self, kwargs: Dict[str, Any]) -> bool:
        return kwargs.get('use_id', True)


class AudioFeatures(BaseDataItem):

    def __init__(self, id: Optional[str], danceability: float, energy: float, key: int, loudness: float, mode: int,
                 speechiness: float, acousticness: float, instrumentalness: float, liveness: float, valence: float,
                 tempo: float, duration_ms: int, time_signature: int, **kwargs):
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
        if self.use_id(kwargs):
            self.id = id

    def add_to_data(self, data: Data) -> Data:
        self.checkattr()
        if not data.tracks[getattr(self, 'id')].audio_features:
            data.tracks[getattr(self, 'id')].audio_features = AudioFeatures(**self.__dict__, use_id=False)
        return data

    @classmethod
    def from_api(cls, audio_features_item: Dict[str, Any]) -> 'AudioFeatures':
        return AudioFeatures(**audio_features_item)

    def check(self) -> bool:
        return False

    @staticmethod
    def attr_names() -> Iterable[str]:
        return [
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

    @property
    def toList(self) -> Iterable[Any]:
        return [getattr(self, atr) for atr in self.attr_names()]

    @classmethod
    def to_df(cls, data: Data) -> pd.DataFrame:
        _data = [
            [track_id, *track.audio_features.toList] for track_id, track in data.tracks.items() if track.audio_features
        ]
        return pd.DataFrame.from_records(_data, columns=['idx', *AudioFeatures.attr_names()])


class Track(BaseDataItem):

    def __init__(self,
                 title: str,
                 artists_ids: Set[str],
                 lyrics: Optional[str] = None,
                 audio_features: Optional[AudioFeatures] = None,
                 id: Optional[str] = None,
                 **kwargs):
        self.title = preprocess_title(title)
        self.artists_ids = artists_ids if artists_ids else set()
        self.lyrics = lyrics
        self.audio_features = audio_features
        if self.use_id(kwargs):
            self.id = id

    def add_to_data(self, data: Data) -> Data:
        self.checkattr()
        if self.id not in data.tracks:
            data.tracks[getattr(self, 'id')] = Track(**self.__dict__, use_id=False)
        return data

    def check(self) -> bool:
        return all(hasattr(self, attr) for attr in ['title', 'lyrics', 'artists_ids']) and not hasattr(self, 'id')

    @classmethod
    def from_api(cls, track_item: Dict[str, Any]) -> 'Track':
        artists_ids = set(artist_info['id'] for artist_info in track_item['artists'])
        title = track_item['name']
        del track_item['artists']
        return Track(title, artists_ids, **track_item)


class Playlist(BaseDataItem):

    def __init__(self, username: str, id: str, name: str, tracks: Optional[Set[str]] = None, **kwargs):
        self.username = username
        self.tracks = tracks if tracks else set()
        self.name = name
        if self.use_id(kwargs):
            self.id = id

    def add_to_data(self, data: Data) -> Data:
        self.checkattr()
        if self.id not in data.playlists:
            data.playlists[self.id] = Playlist(**self.__dict__, use_id=False)
        return data

    def check(self) -> bool:
        return all(hasattr(self, attr) for attr in ['username', 'name', 'tracks']) and not hasattr(self, 'id')

    @classmethod
    def from_api(self, playlist_item: Dict[str, Any]) -> 'Playlist':
        username = playlist_item['owner']['id']
        del playlist_item['tracks']
        return Playlist(username, **playlist_item)


class Artist(BaseDataItem):

    def __init__(self, name: str, albums_id: Optional[Set[str]] = None, id: Optional[str] = None, **kwargs):
        self.name = name
        self.albums_id = albums_id if albums_id else set()
        if self.use_id(kwargs):
            self.id = id

    def add_to_data(self, data: Data) -> Data:
        self.checkattr()
        if self.id not in data.artists:
            data.artists[getattr(self, 'id')] = Artist(**self.__dict__, use_id=False)
        return data

    def check(self) -> bool:
        return all(hasattr(self, attr) for attr in ['name', 'albums_id']) and not hasattr(self, 'id')

    @classmethod
    def from_api(self, artist_item: Dict[str, Any]) -> 'Artist':
        return Artist(**artist_item)

    @classmethod
    def download_info_about_artist(cls, sp, artist_id: str) -> 'Artist':
        artist_info = sp.artist(artist_id)
        return Artist.from_api(artist_info)


class Album(BaseDataItem):

    def __init__(self,
                 name: str,
                 artists_id: Optional[Set[str]] = None,
                 tracks: Optional[Set[str]] = None,
                 id: Optional[str] = None,
                 **kwargs):
        self.artists_id = artists_id if artists_id else set()
        self.name = name
        self.tracks = tracks if tracks else set()
        if self.use_id(kwargs):
            self.id = id

    def add_to_data(self, data: Data) -> Data:
        self.checkattr()
        if self.id not in data.albums:
            data.albums[getattr(self, 'id')] = Album(**self.__dict__, use_id=False)
        return data

    def check(self) -> bool:
        return all(hasattr(self, attr) for attr in ['artists_id', 'name']) and not hasattr(self, 'id')

    @classmethod
    def from_api(self, album_item: Dict[str, Any]) -> 'Album':
        artists_id = set(artist['id'] for artist in album_item['artists'])
        return Album(artists_id=artists_id, **album_item)


class Data:

    def __init__(self,
                 playlists: Optional[Dict[str, Playlist]] = None,
                 tracks: Optional[Dict[str, Track]] = None,
                 artists: Optional[Dict[str, Artist]] = None,
                 albums: Optional[Dict[str, Album]] = None,
                 **_):
        self.playlists = playlists if playlists else dict()
        self.tracks = tracks if tracks else dict()
        self.artists = artists if artists else dict()
        self.albums = albums if albums else dict()

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Data':
        _data = {k: data[k] for k in ['playlists', 'tracks', 'artists', 'albums'] if data.get(k)}
        return Data(**_data)
