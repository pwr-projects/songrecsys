from typing import Sequence, Text


class Playlist:
    def __init__(self,
                 name: Text,
                 tracks: Sequence = list(),
                 use_kwargs: bool = True,
                 **kwargs):
        self.name = name
        self.tracks = tracks

        if use_kwargs:
            self.__dict__.update(kwargs)
