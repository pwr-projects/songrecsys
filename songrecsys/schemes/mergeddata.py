from typing import Sequence

from songrecsys.schemes.playlist import Playlist
from songrecsys.schemes.track import Track


class MergedData(list):
    def __init__(self,
                 item: Sequence):
        all_playlists = all(map(lambda item: type(item) is Playlist, item))
        if all_playlists:
            super().__init__(item)
        else:
            for item in data:
                item['tracks'] = [Track(**tr_info) for tr_info in item['tracks'] if tr_info]
                self.append(Playlist(**item))
