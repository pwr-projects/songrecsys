from typing import List, Union

import numpy as np
from pprint import pprint
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
                return Playlist(id=pl_id, name=pl['name'])
            return None

        api_pls = self._api.user_playlists(username, limit=min(50, max_count))

        while api_pls:
            self._data.playlists.get(username).extend(list(filter(None, map(filter_playlist_info, api_pls['items']))))
            api_pls = self._api.next(api_pls) if api_pls['next'] else None

        dump(self._data)

        return self._data

    def get_tracks_from_playlists(self, username: str, update:bool, save_interval: int = 20) -> Data:
        text_prefix = 'Getting tracks from playlists'
        with tqdm(tuple(enumerate(self._data.playlists.get(username))), text_prefix) as pbar:

            for _, pl in pbar:
                pbar.set_description(f'{text_prefix} - tracks count: {len(self._data.tracks)}')

                tracks = self._extract_tr_info_from_pl(username, pl.id)
                pl.tracks = set(pl.tracks)
                for track in filter(None, tracks):
                    track_id = track.get('id')
                    if update or track_id not in self._data.tracks.keys():
                        self._data.tracks[track_id] = Track(**{
                            key: track.get(key)
                            for key in ['title', 'artists', 'lyrics', 'artists_ids']
                            if track.get(key)
                        })

                        pl.tracks.add(track_id)

                # if interval_cnt % save_interval == 0:
                #     pbar.set_description(f'{text_prefix} - saving')
                #     dump(self._data, verbose=False)

        dump(self._data)
        return self._data

    def get_all_playlists_and_tracks_of_user(self, username: str, update:bool, max_playlist_count: int = np.inf) -> Data:
        self.get_all_playlists_of_user(username, max_playlist_count)
        self.get_tracks_from_playlists(username, update)
        return self._data

    def download_data(self, update: bool = False) -> Data:
        for username in self._api.usernames:
            self.get_all_playlists_and_tracks_of_user(username, update)

    def _extract_tr_info_from_pl(self, username: str, playlist_id: str) -> List[dict]:
        parse_track_info = lambda tracks: list(map(self._extract_specific_info_from_track_item, tracks['items']))

        results = self._api.user_playlist(username, playlist_id, fields='tracks,next')

        tracks = results['tracks']
        all_tracks_info = parse_track_info(tracks)

        while tracks['next']:
            tracks = self._api.next(tracks)
            tracks_info = parse_track_info(tracks)
            all_tracks_info.extend(list(tracks_info))

        return all_tracks_info

    def _extract_specific_info_from_track_item(self, track_item: dict) -> Union[Track, None]:
        track_info = track_item.get('track')

        if not track_info:
            return None

        song_id = track_info['id']
        artists = list(map(lambda artist_info: artist_info['name'], track_info['artists']))
        artists_ids = list(map(lambda artist_info: artist_info['id'], track_info['artists']))
        title = track_info['name']
        return dict(id=song_id, title=title, artists=artists, artists_ids=artists_ids)
