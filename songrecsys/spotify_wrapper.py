from typing import Sequence, Text, Dict

import spotipy.util as util
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.util import prompt_for_user_token
from tqdm import tqdm

import numpy as np

from .config import ConfigBase


class SpotifyWrapper(Spotify):
    def __init__(self, config: ConfigBase, username: Text, *args, **kwargs):
        auth = SpotifyClientCredentials(client_id=config.config.client_id,
                                        client_secret=config.config.client_secret)
        super().__init__(client_credentials_manager=auth,
                         *args, **kwargs)

        self._username = username

    def get_all_playlists_of_user(self, max_count: int = np.inf) -> Sequence[Text]:
        playlist_ids = []
        playlists = self.user_playlists(self._username, limit=min(50, max_count))

        print(f'Getting playlists of user: {self._username}...')

        while playlists and len(playlist_ids) < max_count:
            ids = map(lambda playlist: playlist['id'], playlists['items'])
            playlist_ids.extend(list(ids))
            playlists = self.next(playlists) if playlists['next'] else None
            print(f'{len(playlist_ids)} playlists', flush=True, end='\r')
        print()

        return playlist_ids

    def get_tracks_from_playlists(self, *playlist_ids: Sequence[Text]) -> Sequence[Dict]:
        all_playlists_info = {}

        for playlist_id in tqdm(playlist_ids, 'Getting songs from playlists', leave=False):
            all_playlists_info[playlist_id] = self._extract_tracks_info_from_playlist(playlist_id)

        return all_playlists_info

    def _extract_tracks_info_from_playlist(self, playlist_id: Text) -> Sequence:
        parse_track_info = lambda tracks: list(map(self._extract_specific_info_from_track_item, tracks['items']))

        results = self.user_playlist(self._username,
                                     playlist_id,
                                     fields='tracks,next')

        tracks = results['tracks']
        all_tracks_info = parse_track_info(tracks)

        while tracks['next']:
            tracks = self.next(tracks)
            tracks_info = parse_track_info(tracks)
            all_tracks_info.extend(list(tracks_info))

        return all_tracks_info

    def _extract_specific_info_from_track_item(self, track_item: Dict) -> Dict:
        track_info = track_item.get('track')

        if not track_info:
            return None

        song_id = track_info['id']
        artists = list(map(lambda artist_info: artist_info['name'], track_info['artists']))
        title = track_info['name']

        return {'id': song_id,
                'title': title,
                'artists': artists}

# permitions for user data
# ['user-read-private', 'user-read-birthdate', 'user-read-email', 'playlist-read-private', 'user-library-read', 'user-library-modify', 'user-top-read', 'playlist-read-collaborative', 'playlist-modify-public',
#     'playlist-modify-private', 'user-follow-read', 'user-follow-modify', 'user-read-currently-playing', 'user-modify-playback-state', 'user-read-recently-played', 'user-read-playback-state']
