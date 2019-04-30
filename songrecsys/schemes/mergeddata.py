from typing import Sequence

from songrecsys.schemes.playlist import Playlist
from songrecsys.schemes.track import Track


class MergedData(list):
    def __init__(self,
                 data: Sequence):
        all_playlists = all(map(lambda item: type(item) is Playlist, data))
        if all_playlists:
            super().__init__(data)
        else:
            for item in data:
                item['tracks'] = [Track(**tr_info) for tr_info in item['tracks'] if tr_info]
                self.append(Playlist(**item))
