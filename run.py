from pprint import pprint

from songrecsys import *
from tqdm import tqdm

if __name__ == '__main__':
    config = ConfigMgr(CONFIG_DEFAULT_PATH)
    sp = SpotifyWrapper(config)
    
    playlist_ids = sp.get_all_playlists_of_user('spotify')  
    songs = sp.get_tracks_from_playlists('spotify', *playlist_ids)