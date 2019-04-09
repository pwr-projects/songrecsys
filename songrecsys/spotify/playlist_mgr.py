import os
from pprint import pprint
from typing import Dict, Sequence, Text

import numpy as np
from spotipy import Spotify
from tqdm import tqdm

from songrecsys.consts import DEFAULT_PATH_PLAYLISTS
from songrecsys.spotify.spotify_wrapper import SpotifyWrapper
from songrecsys.utils import load_from_json, save_to_json


class PlaylistMgr:
    def __init__(self, spotify_api: SpotifyWrapper):
        self._api = spotify_api

    def get_all_playlists_of_user(self, max_count: int = np.inf) -> Sequence[Text]:
        playlist_info = []
        pl_infos = self._api.user_playlists(self._api.username, limit=min(50, max_count))

        print(f"Getting playlists of user: {self._api.username}...")

        while pl_infos and len(playlist_info) < max_count:
            playlist_info.extend([{ "id": pl_info["id"], "name": pl_info["name"]} for pl_info in pl_infos["items"]])
            pl_infos = self._api.next(pl_infos) if pl_infos["next"] else None
            print(f"{len(playlist_info)} playlists", flush=True, end="\r")
        print()

        return playlist_info

    def get_tracks_from_playlists(self, *playlist_infos: Sequence[Dict]) -> Sequence[Dict]:

        for pl_info in tqdm(playlist_infos, "Getting songs from playlists", leave=False):
            pl_info["tracks"] = self._extract_tracks_info_from_playlist(pl_info["id"])

        return playlist_infos

    def get_all_playlists_and_tracks(self,
                                     save: bool = True,
                                     where_to_save: Text = DEFAULT_PATH_PLAYLISTS,
                                     load_saved: bool = True,
                                     max_playlist_count: int = np.inf) -> Dict[Text, Sequence]:
        if load_saved and os.path.exists(where_to_save):
            return load_from_json(where_to_save)

        pl_infos = self.get_all_playlists_of_user(max_playlist_count)
        songs = self.get_tracks_from_playlists(*pl_infos)
        return save_to_json(songs, where_to_save) if save else songs

    def _extract_tracks_info_from_playlist(self, playlist_id: Text) -> Sequence:
        def parse_track_info(tracks):
            return list(map(self._extract_specific_info_from_track_item,
                            tracks["items"]))

        results = self._api.user_playlist(self._api.username, playlist_id, fields="tracks,next")

        tracks = results["tracks"]
        all_tracks_info = parse_track_info(tracks)

        while tracks["next"]:
            tracks = self._api.next(tracks)
            tracks_info = parse_track_info(tracks)
            all_tracks_info.extend(list(tracks_info))

        return all_tracks_info

    def _extract_specific_info_from_track_item(self, track_item: Dict) -> Dict:
        track_info = track_item.get("track")

        if not track_info:
            return None

        song_id = track_info["id"]
        artists = list(map(lambda artist_info: artist_info["name"], track_info["artists"]))
        title = track_info["name"]

        return {"id": song_id, "title": title, "artists": artists}


    def summary(self, playlists):
        all_tracks = 0
        for pl_info in playlists:
            tracks_no = len(pl_info["tracks"])
            all_tracks += tracks_no
            print(f'\t{pl_info["name"]} - {tracks_no} tracks')
        print(f'Downloaded {len(playlists)} playlists. Overall: {all_tracks} tracks.')