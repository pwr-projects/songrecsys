from typing import Text, Sequence


class TrackBase:
    def __init__(self, id: Text,
                 title: Text,
                 artists: Sequence[Text],
                 lyrics: Text):
        setattr(self, 'id', id)
        setattr(self, 'title', title)
        setattr(self, 'artists', artists)
        setattr(self, 'lyrics', lyrics)


class PlaylistBase:
    def __init__(self, id: Text,
                 name: Text,
                 tracks: Sequence):
        setattr(self, 'id', id)
        setattr(self, 'name', name)
        setattr(self, 'tracks', list(map(TrackBase, tracks)))

class Dataset:
    def __init__(self, json_data):
        setattr(self, )
