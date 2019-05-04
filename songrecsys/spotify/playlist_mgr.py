from pprint import pprint
from time import sleep
from typing import List, Union

import numpy as np
from spotipy import SpotifyException

from songrecsys.data.manager import dump
from songrecsys.schemes import Data, Playlist, Track
from songrecsys.spotify.spotify_wrapper import SpotifyWrapper
from songrecsys.utils.utils import tqdm


class PlaylistMgr:

    def __init__(self, spotify_api: SpotifyWrapper, data: Data = Data()):
        self._api = spotify_api
        self._data: Data = data

    def get_all_playlists_of_user(self, username: str, max_count: int = np.inf) -> Data:
        # print(f'Downloading playlist of {username}', end='... ')

        pls_ids = set(map(lambda pl: pl.id, self._data.playlists[username]))

        def filter_playlist_info(pl: dict):
            pl_id = pl['id']
            if pl_id not in pls_ids:
                pls_ids.add(pl_id)
                return Playlist(**pl)
            return None

        api_pls = self._api.user_playlists(username, limit=min(50, max_count))

        while api_pls:
            self._data.playlists.get(username).extend(list(filter(None, map(filter_playlist_info, api_pls['items']))))
            api_pls = self._api.next(api_pls) if api_pls['next'] else None

        dump(self._data)

        return self._data

    def get_tracks_from_playlists(self, username: str, update: bool, save_interval: int = 50) -> Data:
        text_prefix = 'Getting tracks from playlists'
        with tqdm(tuple(enumerate(self._data.playlists.get(username))), text_prefix) as pbar:
            for interval_cnt, pl in pbar:
                pbar.set_description(f'{text_prefix} - tracks count: {len(self._data.tracks)}')
                pl.tracks = set(pl.tracks)
                tracks = self._extract_tr_info_from_pl(username, pl.id)
                for track in filter(None, tracks):
                    track.add_to_data(self._data)
                    pl.tracks.add(track.id)

                if interval_cnt % save_interval == 0:
                    pbar.set_description(f'{text_prefix} - saving')
                    dump(self._data, verbose=False)
                sleep(0.2)
        dump(self._data)
        return self._data

    def get_all_playlists_and_tracks_of_user(self, username: str, update: bool,
                                             max_playlist_count: int = np.inf) -> Data:
        self.get_all_playlists_of_user(username, max_playlist_count)
        self.get_tracks_from_playlists(username, update)
        return self._data

    def download_data(self, update: bool = False) -> Data:
        for username in self._api.usernames:
            self.get_all_playlists_and_tracks_of_user(username, update)

    def _extract_tr_info_from_pl(self, username: str, playlist_id: str) -> List[Track]:
        try:
            tracks = self._api.user_playlist(username, playlist_id, fields='tracks,next')
        except SpotifyException as e:
            print(e)
            return []

        all_tracks_info: list = list()

        while tracks:
            all_tracks_info.extend(filter(None, map(lambda item: item.get('track'), tracks.get('tracks').get('items'))))
            tracks = self._api.next(tracks) if tracks.get('next') else None

        return list(map(self.extract_specific_info_from_track_item, all_tracks_info))

    @classmethod
    def extract_specific_info_from_track_item(cls, track_item: dict) -> Track:
        artists = list(map(lambda artist_info: artist_info['name'], track_item['artists']))
        artists_ids = list(map(lambda artist_info: artist_info['id'], track_item['artists']))
        title = track_item['name']
        del track_item['artists']
        return Track(title, artists, artists_ids, **track_item)
