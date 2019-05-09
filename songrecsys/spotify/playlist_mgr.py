from pprint import pprint
from sys import stdout
from time import sleep
from typing import List, Union

import numpy as np
from spotipy import SpotifyException

from songrecsys.data import dump
from songrecsys.schemes import Data, Playlist, Track
from songrecsys.spotify.spotify_wrapper import SpotifyWrapper
from songrecsys.utils import tqdm
from songrecsys.config import ConfigBase


class PlaylistMgr:

    def __init__(self, spotify_api: SpotifyWrapper, config: ConfigBase, data: Data = Data(), override: bool = True):
        self._api = spotify_api
        self._config = config
        self._data: Data = data
        self._override = override

    def download_all_playlists_of_user(self, username: str, max_count: int = np.inf) -> Data:
        stdout.write(f'Downloading playlist of {username}... ')
        stdout.flush()

        all_playlists: List[dict] = list()
        api_pls = self._api.user_playlists(username, limit=min(50, max_count))

        while api_pls:
            all_playlists.extend(api_pls['items'])
            if api_pls.get('next'):
                sleep(self._config.request_interval)
                api_pls = self._api.next(api_pls)
            else:
                api_pls = None

        for playlist in all_playlists:
            Playlist.from_api(playlist).add_to_data(self._data, self._override)

        print(f'{len(self._data.playlists)} playlists')

        return dump(self._data)

    def download_tracks_info_of_playlists(self, username: str, update: bool, save_interval: int = 50) -> Data:
        text_prefix = 'Getting tracks from playlists'
        with tqdm(tuple(enumerate(self._data.playlists)), text_prefix) as pbar:
            for interval_cnt, pl in pbar:
                sleep(self._config.request_interval)
                pbar.set_description(f'{text_prefix} - tracks count: {len(self._data.tracks)}')

                tracks = self._extract_tr_info_from_pl(username, pl)

                for track in tracks:
                    track.add_to_data(self._data, self._override)
                    self._data.playlists[pl].tracks.add(track.id)

                if interval_cnt % save_interval == 0:
                    pbar.set_description(f'{text_prefix} - saving')
                    dump(self._data, verbose=False)

        return dump(self._data)

    def get_all_playlists_and_tracks_of_user(self, username: str, update: bool,
                                             max_playlist_count: int = np.inf) -> Data:
        self.download_all_playlists_of_user(username, max_playlist_count)
        self.download_tracks_info_of_playlists(username, update)
        return self._data

    def download_data(self, update: bool = False) -> Data:
        for username in self._api.usernames:
            self.get_all_playlists_and_tracks_of_user(username, update)

    def _extract_tr_info_from_pl(self, username: str, playlist_id: str, delete_on_fail: bool = False) -> List[Track]:
        try:
            tracks = self._api.user_playlist(username, playlist_id, fields='tracks,next')
            all_tracks_info = list()

            while tracks:
                all_tracks_info.extend(
                    filter(None, map(lambda item: item.get('track'),
                                     tracks.get('tracks').get('items'))))
                tracks = self._api.next(tracks) if tracks.get('next') else None
            return list(filter(None, map(Track.from_api, all_tracks_info)))
        except Exception as e:
            if delete_on_fail:
                del self._data.playlists[playlist_id]
            print(e)
            return None
