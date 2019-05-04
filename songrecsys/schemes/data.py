import re
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import List, NoReturn, Set


class BaseDataItem(ABC):

    def checkattr(self, name: str = 'id'):
        if not hasattr(self, name):
            raise f'Cannot add to data because there is no `{name}` attribute'

    @abstractmethod
    def add_to_data(self, data) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    def check(self) -> bool:
        raise NotImplementedError


class Track(BaseDataItem):

    def __init__(self,
                 title: str = None,
                 artists: Set[str] = None,
                 artists_ids: Set[str] = None,
                 lyrics: str = None,
                 id: str = None,
                 use_id: bool = True,
                 **_):
        if use_id:
            self.id = id
        if title:
            title = re.sub(r"\(.*\)|\[.*\]", '', title)  # (feat.) [extended cut]
            title = re.sub(r"-.*", '', title)  # - Remastered ...
            self.title: str = title
        if artists:
            self.artists: Set[str] = artists
        if artists_ids:
            self.artists_ids: Set[str] = artists_ids
        self.lyrics: str = lyrics

    def add_to_data(self, data) -> NoReturn:
        self.checkattr()
        # if self.id not in data.tracks:
        data.tracks[self.id] = Track(**self.__dict__, use_id=False)

    def check(self) -> bool:
        return all(map(lambda attr: hasattr(self, attr), ['title', 'artists', 'lyrics', 'artists_ids']))


class Playlist(BaseDataItem):

    def __init__(self,
                 username: str = None,
                 id: str = None,
                 name: str = None,
                 tracks: Set[str] = None,
                 use_username: bool = True,
                 **_):
        if use_username:
            self.username = username
        self.id: str = id
        self.name: str = name
        if tracks:
            self.tracks: Set[str] = tracks

    def add_to_data(self, data) -> NoReturn:
        self.checkattr('username')
        if self.id not in map(lambda pl: pl.id, data.playlists[self.username]):
            data.playlists[self.username].append(Playlist(**self.__dict__, use_username=False))

    def check(self) -> bool:
        return all(map(lambda attr: hasattr(self, attr), ['id', 'name', 'tracks']))


class Artist(BaseDataItem):

    def __init__(self, name: str, albums_id: List[str] = None, id: str = None, use_id: bool = True, **_):
        self.name = name
        if albums_id:
            self.albums_id = albums_id
        if use_id:
            self.id = id

        self.albums_downloaded: bool = False

    def add_to_data(self, data) -> NoReturn:
        self.checkattr()
        if self.id not in data.artists:
            data.artists[self.id] = Artist(**self.__dict__, use_id=False)

    def check(self) -> bool:
        return all(map(lambda attr: hasattr(self, attr), ['name', 'albums_id']))


class Album(BaseDataItem):

    def __init__(self,
                 id: str = None,
                 artists_id: List[str] = None,
                 tracks: List[str] = None,
                 name: str = None,
                 use_id: bool = True,
                 **_):
        if use_id:
            self.id = id
        self.artists_id = artists_id
        self.name = name
        self.tracks = tracks

    def add_to_data(self, data):
        self.checkattr()
        if self.id not in data.albums:
            data.albums[self.id] = Album(**self.__dict__, use_id=False)

    def check(self) -> bool:
        return all(map(lambda attr: hasattr(self, attr), ['artists_id', 'name']))


class Data:

    def __init__(self,
                 playlists: dict = defaultdict(list),
                 tracks: dict = defaultdict(Track),
                 artists: dict = defaultdict(Artist),
                 albums: dict = defaultdict(Album),
                 **_):
        self.playlists = playlists
        self.tracks = tracks
        self.artists = artists
        self.albums = albums
