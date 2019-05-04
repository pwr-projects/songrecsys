from collections import defaultdict
from typing import List, Set


class Track:

    def __init__(self, title: str = None, artists: Set[str] = set(), artists_ids: Set[str] = set(), lyrics: str = None):
        self.title: str = title
        self.artists: Set[str] = artists
        self.lyrics: str = lyrics
        self.artists_ids: Set[str] = artists_ids


class Playlist:

    def __init__(self, id: str, name: str, tracks: Set[str] = set()):
        self.id: str = id
        self.name: str = name
        self.tracks: Set[str] = tracks


class Artist:

    def __init__(self, name: str):
        self.name = name


class Data:

    def __init__(self, playlists: dict = None, tracks: dict = None, artists: dict = None):
        self.playlists = playlists if playlists else defaultdict(list)
        self.tracks = tracks if tracks else defaultdict(Track)
        self.artists = artists if artists else defaultdict(Artist)

    @classmethod
    def from_json(cls, data: dict):
        return Data(data['playlists'], data['tracks'], data['artists'])
