from typing import List, Union

import numpy as np

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

        pls_ids = list(map(lambda pl: pl.id, self._data.playlists.get(username)))

        def filter_playlist_info(pl: dict):
            pl_id = pl['id']
            if pl_id not in pls_ids:
                pls_ids.append(pl_id)
                return Playlist(id=pl_id, name=pl['name'])
            return None

        api_pls = self._api.user_playlists(username, limit=min(50, max_count))

        while api_pls:
            self._data.playlists.get(username).extend(filter(None, map(filter_playlist_info, api_pls['items'])))
            api_pls = self._api.next(api_pls) if api_pls['next'] else None

        return self._data

    def get_tracks_from_playlists(self, username: str, save_interval: int = 20) -> Data:
        tracks_sum = 0
        text_prefix = 'Getting tracks from playlists'
        with tqdm(enumerate(self._data.playlists.get(username)), text_prefix) as pbar:
            for interval_cnt, pl in pbar:
                tracks = self._extract_tr_info_from_pl(username, pl.id)

                for track in tracks:
                    data.tracks[track['id']] = Track(**{key: track[key] for key in ['title', 'artists', 'lyrics']})
                    pl.tracks.append(track['id'])

                if interval_cnt == save_interval:
                    dump(merged_data=self._data)
                    interval_cnt = 0

                tracks_sum += len(pl.tracks)
                pbar.set_description(f'{text_prefix} - {tracks_sum} tracks')
        dump(merged_data=self._data)
        return self._data

    def get_all_playlists_and_tracks_of_user(self, username: str, save: bool = True, max_playlist_count: int = np.inf) -> Data:
        self.get_all_playlists_of_user(username, max_playlist_count)
        self.get_tracks_from_playlists(username)
        return self._data

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
        title = track_info['name']
        return dict(id=song_id, title=title, artists=artists)
