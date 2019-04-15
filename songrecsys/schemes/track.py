from typing import Sequence, Text


class Track:
    def __init__(self,
                 title: Text,
                 artists: Sequence[Text],
                 lyrics: Text = None,
                 use_kwargs: bool = True,
                 **kwargs):
        self.title = title
        self.artists = artists
        self.lyrics = lyrics

        if use_kwargs:
            self.__dict__.update(kwargs)
