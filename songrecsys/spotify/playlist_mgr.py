import os
from typing import Dict, Sequence, Text

import numpy as np
from spotipy import Spotify
from tqdm import tqdm

from songrecsys.consts import DEFAULT_PATH_PLAYLISTS
from songrecsys.utils import load_from_json, save_to_json


class PlaylistMgr:
    def __init__(self, spotify_api):
        self._spotify_api = spotify_api

    def get_all_playlists_of_user(self, max_count: int = np.inf) -> Sequence[Text]:
        playlist_ids = []
        playlists = self._spotify_api.user_playlists(self._spotify_api.username, limit=min(50, max_count))

        print(f"Getting playlists of user: {self._spotify_api.username}...")

        while playlists and len(playlist_ids) < max_count:
            ids = map(lambda playlist: playlist["id"], playlists["items"])
            playlist_ids.extend(list(ids))
            playlists = self._spotify_api.next(playlists) if playlists["next"] else None
            print(f"{len(playlist_ids)} playlists", flush=True, end="\r")
        print()

        return playlist_ids

    def get_tracks_from_playlists(self, *playlist_ids: Sequence[Text]) -> Sequence[Dict]:
        all_playlists_info = {}

        for playlist_id in tqdm(playlist_ids, "Getting songs from playlists", leave=False):
            all_playlists_info[playlist_id] = self._extract_tracks_info_from_playlist(playlist_id)

        return all_playlists_info

    def get_all_playlists_and_tracks(self,
                                     save: bool = True,
                                     where_to_save: Text = DEFAULT_PATH_PLAYLISTS,
                                     load_saved: bool = True) -> Dict[Text, Sequence]:
        if load_saved and os.path.exists(where_to_save):
            return load_from_json(where_to_save)

        playlist_ids = self.get_all_playlists_of_user()
        songs = self.get_tracks_from_playlists(*playlist_ids)
        return save_to_json(songs, where_to_save) if save else songs

    def _extract_tracks_info_from_playlist(self, playlist_id: Text) -> Sequence:
        def parse_track_info(tracks):
            return list(map(self._extract_specific_info_from_track_item,
                            tracks["items"]))

        results = self._spotify_api.user_playlist(self._spotify_api.username, playlist_id, fields="tracks,next")

        tracks = results["tracks"]
        all_tracks_info = parse_track_info(tracks)

        while tracks["next"]:
            tracks = self._spotify_api.next(tracks)
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
