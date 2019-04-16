import os
from pprint import pprint
from typing import Dict, NoReturn, Sequence, Text, Tuple

import numpy as np
from spotipy import Spotify
from tqdm import tqdm

from songrecsys.consts import (DEFAULT_PATH_MERGED_DATA,
                               DEFAULT_PATH_PLAYLISTS, DEFAULT_PATH_TRACKS)
from songrecsys.schemes.mergeddata import MergedData
from songrecsys.schemes.playlist import Playlist
from songrecsys.schemes.track import Track
from songrecsys.spotify.spotify_wrapper import SpotifyWrapper
from songrecsys.utils import dump, load


class PlaylistMgr:
    def __init__(self, spotify_api: SpotifyWrapper):
        self._api = spotify_api

    def get_all_playlists_of_user(self,
                                  max_count: int = np.inf,
                                  data: MergedData = None) -> Sequence[Text]:
        pls = data if data else list()
        pls_ids = list(map(lambda pl: pl.id, data)) if data else list()

        def filter_playlist_info(pl):
            pl_id = pl['id']
            if pl_id not in pls_ids:
                pls_ids.append(pl_id)
                return Playlist(id=pl['id'], name=pl['name'])
            return None

        print(f'Downloading playlist of {self._api.username}', end='... ')

        api_pls = self._api.user_playlists(self._api.username, limit=min(50, max_count))
        while api_pls and len(pls) < max_count:
            pls.extend(filter(None, map(filter_playlist_info, api_pls['items'])))
            api_pls = self._api.next(api_pls) if api_pls['next'] else None
        print(f'{len(pls)} playlists')

        return pls

    def get_tracks_from_playlists(self,
                                  pls: Sequence[Playlist],
                                  save_interval: int = 20) -> Sequence[Dict]:
        interval_cnt = 0
        for pl in tqdm(pls, 'Getting tracks from playlists', leave=False):
            if not pl.tracks:
                pl.tracks = self._extract_tr_info_from_pl(pl.id)
                interval_cnt += 1
            if interval_cnt == save_interval:
                dump(merged_data=pls)
                interval_cnt = 0
        return pls

    def get_all_playlists_and_tracks(self,
                                     save: bool = True,
                                     load_saved: bool = True,
                                     update: bool = True,
                                     max_playlist_count: int = np.inf) -> Tuple:
        loaded_data = None
        if load_saved:
            loaded_data = load(playlists=True, tracks=True, merged_data=True)

            if 'playlists' in loaded_data and 'tracks' in loaded_data:
                loaded_data = self.merge_data(loaded_data['playlists'], loaded_data['tracks'])
            elif 'merged_data' in loaded_data:
                loaded_data = loaded_data.get('merged_data')

            print(f'Loaded {len(loaded_data)} playlists')
            if not update:
                return self.split_merged_data(loaded_data)
            else:
                print('Updating loaded data...')

        pls = self.get_all_playlists_of_user(max_playlist_count, loaded_data)
        merged_data = MergedData(self.get_tracks_from_playlists(pls))
        playlists, tracks = self.split_merged_data(merged_data)

        if save:
            dump(merged_data=merged_data, playlists=playlists, tracks=tracks)

        return playlists, tracks

    def _extract_tr_info_from_pl(self, playlist_id: Text) -> Sequence:
        parse_track_info = lambda tracks: list(map(self._extract_specific_info_from_track_item,
                                                   tracks['items']))

        results = self._api.user_playlist(self._api.username,
                                          playlist_id,
                                          fields='tracks,next')

        tracks = results['tracks']
        all_tracks_info = parse_track_info(tracks)

        while tracks['next']:
            tracks = self._api.next(tracks)
            tracks_info = parse_track_info(tracks)
            all_tracks_info.extend(list(tracks_info))

        return all_tracks_info

    def _extract_specific_info_from_track_item(self, track_item: Dict) -> Dict:
        track_info = track_item.get('track')

        if not track_info:
            return None

        song_id = track_info['id']
        artists = list(map(lambda artist_info: artist_info['name'],
                           track_info['artists']))
        title = track_info['name']

        return Track(id=song_id, title=title, artists=artists)

    def split_merged_data(self,
                          merged_data: MergedData,
                          save: bool = True) -> Tuple:
        playlists, tracks = {}, {}

        for pl in tqdm(merged_data, 'Spliting: playlists', leave=False):

            new_tracks = []
            for pl_tr in tqdm(pl.tracks, 'Spliting: tracks', leave=False):
                new_tracks.append(pl_tr.id)
                tracks[pl_tr.id] = Track(**pl_tr.__dict__, use_kwargs=False)

            new_playlist = Playlist(**pl.__dict__, use_kwargs=False)
            new_playlist.tracks = new_tracks
            playlists[pl.id] = new_playlist

        if save:
            dump(playlists=playlists, tracks=tracks)

        return playlists, tracks

    def merge_data(self,
                   playlists: Dict[Text, Playlist],
                   tracks: Dict[Text, Track],
                   save: bool = True) -> MergedData:
        merged_data = []
        for playlist_id, playlist in playlists.items():
            playlist = Playlist(id=playlist_id, **playlist)
            new_tracks = [Track(id=tr, **tracks[tr]) for tr in playlist.tracks if tr]
            playlist.tracks = new_tracks
            merged_data.append(playlist)

        if save:
            dump(merged_data=merged_data)

        return merged_data
