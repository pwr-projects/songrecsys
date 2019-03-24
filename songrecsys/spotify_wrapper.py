from typing import Sequence, Text

import spotipy.util as util
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.util import prompt_for_user_token
from tqdm import tqdm

import numpy as np

from .config import ConfigBase


def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print('   %d %32.32s %s' % (i, track['artists'][0]['name'],
            track['name']))
class SpotifyWrapper(Spotify):
    def __init__(self, config: ConfigBase, *args, **kwargs):
        auth = SpotifyClientCredentials(client_id=config.config.client_id,
                                        client_secret=config.config.client_secret)
        super().__init__(client_credentials_manager=auth,
                         *args, **kwargs)

    def get_all_playlists_of_user(self, username: Text, max_count:int =np.inf) -> Sequence:
        playlist_ids = []
        playlists = self.user_playlists(username, limit=min(50, max_count))
        
        print(f'Getting playlists of user: {username}...')
        
        while playlists and len(playlist_ids) < max_count:
            ids = map(lambda playlist: playlist['id'], playlists['items'])
            playlist_ids.extend(list(ids))
            playlists = self.next(playlists) if playlists['next'] else None
            print(f'{len(playlist_ids)} playlists', flush=True, end='\r')
        print()

        return playlist_ids

    def get_tracks_from_playlists(self, username, *playlist_ids: Sequence[Text]) -> Sequence:
        all_playlists_info = {}
        for playlist_id in tqdm(playlist_ids, 'Getting songs from playlists', leave=False):
            results = self.user_playlist(username, 
                                    playlist_id,
                            fields='tracks,next')

            tracks = results['tracks']
            all_tracks_info = tracks['items']

            while tracks['next']:
                tracks = self.next(tracks)
                # TODO Extract only needed data
                all_tracks_info.extend(tracks['items'])

            all_playlists_info[playlist_id] = all_tracks_info

        return all_playlists_info




# permitions for user data
# ['user-read-private', 'user-read-birthdate', 'user-read-email', 'playlist-read-private', 'user-library-read', 'user-library-modify', 'user-top-read', 'playlist-read-collaborative', 'playlist-modify-public',
#     'playlist-modify-private', 'user-follow-read', 'user-follow-modify', 'user-read-currently-playing', 'user-modify-playback-state', 'user-read-recently-played', 'user-read-playback-state']
