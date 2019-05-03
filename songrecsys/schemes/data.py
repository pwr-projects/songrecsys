from collections import defaultdict
from typing import List


class Track:

    def __init__(self, title: str = None, artists: List[str] = list(), lyrics: str = None):
        self.title: str = title
        self.artists: List[str] = artists
        self.lyrics: str = lyrics


class Playlist:

    def __init__(self, id: str, name: str, tracks: List[str] = list()):
        self.id: str = id
        self.name: str = name
        self.tracks: List[str] = tracks


class Data:

    def __init__(self, playlists: dict = None, tracks: dict = None):
        self.playlists = playlists if playlists else defaultdict(list)
        self.tracks = tracks if tracks else defaultdict(Track)

    @classmethod
    def from_json(cls, data: dict):
        return Data(data['playlists'], data['tracks'])
