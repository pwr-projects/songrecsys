import re
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import List, NoReturn, Set

from songrecsys.nlp import preprocess_title


class BaseDataItem(ABC):

    def checkattr(self, name: str = 'id'):
        if not hasattr(self, name):
            raise f'Cannot add to data because there is no `{name}` attribute'

    @abstractmethod
    def add_to_data(self, data, override) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    def check(self) -> bool:
        raise NotImplementedError


class Track(BaseDataItem):

    def __init__(self,
                 title: str = None,
                 artists_ids: Set[str] = set(),
                 lyrics: str = None,
                 id: str = None,
                 use_id: bool = True,
                 **_):
        if use_id:
            self.id = id
        self.title: str = preprocess_title(title)
        self.artists_ids: Set[str] = artists_ids
        self.lyrics: str = lyrics

    def add_to_data(self, data, override: bool = True) -> NoReturn:
        self.checkattr()
        if override or self.id not in data.tracks:
            data.tracks[self.id] = Track(**self.__dict__, use_id=False)

    def check(self) -> bool:
        return all(map(lambda attr: hasattr(self, attr),
                       ['title', 'lyrics', 'artists_ids'])) and not hasattr(self, 'id')

    @classmethod
    def from_api(cls, track_item: dict):
        artists_ids = list(map(lambda artist_info: artist_info['id'], track_item['artists']))
        title = track_item['name']
        del track_item['artists']
        return Track(title,  artists_ids, **track_item)


class Playlist(BaseDataItem):

    def __init__(self,
                 username: str = None,
                 id: str = None,
                 name: str = None,
                 tracks: Set[str] = set(),
                 use_id: bool = True,
                 **_):
        self.username = username
        if use_id:
            self.id: str = id
        self.name: str = name
        self.tracks: Set[str] = tracks

    def add_to_data(self, data, override: bool = True) -> NoReturn:
        self.checkattr()
        if override or self.id not in data.playlists:
            data.playlists[self.id] = Playlist(**self.__dict__, use_id=False)

    def check(self) -> bool:
        return all(map(lambda attr: hasattr(self, attr), ['username', 'name', 'tracks'])) and not hasattr(self, 'id')

    @classmethod
    def from_api(self, playlist_item: dict):
        username = playlist_item['owner']['id']
        del playlist_item['tracks']
        return Playlist(username, **playlist_item)


class Artist(BaseDataItem):

    def __init__(self, name: str, albums_id: List[str] = list(), id: str = None, use_id: bool = True, **_):
        self.name = name
        self.albums_id = albums_id
        if use_id:
            self.id = id

    def add_to_data(self, data, override: bool = True) -> NoReturn:
        self.checkattr()
        if override or self.id not in data.artists:
            data.artists[self.id] = Artist(**self.__dict__, use_id=False)

    def check(self) -> bool:
        return all(map(lambda attr: hasattr(self, attr), ['name', 'albums_id'])) and not hasattr(self, 'id')

    @classmethod
    def from_api(self, artist_item: dict):
        return Artist(**artist_item)


class Album(BaseDataItem):

    def __init__(self,
                 id: str = None,
                 artists_id: List[str] = list(),
                 tracks: List[str] = list(),
                 name: str = None,
                 use_id: bool = True,
                 **_):
        if use_id:
            self.id = id
        self.artists_id = artists_id
        self.name = name
        self.tracks = tracks

    def add_to_data(self, data, override):
        self.checkattr()
        if override or self.id not in data.albums:
            data.albums[self.id] = Album(**self.__dict__, use_id=False)

    def check(self) -> bool:
        return all(map(lambda attr: hasattr(self, attr), ['artists_id', 'name'])) and not hasattr(self, 'id')

    @classmethod
    def from_api(self, album_item: dict):
        artists_id = set(map(lambda artist: artist['id'], album_item['artists']))
        return Album(artists_id=artists_id, **album_item)


class Data:

    def __init__(self,
                 playlists: dict = defaultdict(Playlist),
                 tracks: dict = defaultdict(Track),
                 artists: dict = defaultdict(Artist),
                 albums: dict = defaultdict(Album),
                 **_):
        self.playlists = playlists
        self.tracks = tracks
        self.artists = artists
        self.albums = albums

    @classmethod
    def from_json(cls, data: dict):
        _data = {k: data[k] for k in ['playlists', 'tracks', 'artists', 'albums'] if data.get(k)}
        return Data(**_data)
