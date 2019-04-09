#!.env/bin/python
from pprint import pprint
from typing import Dict, Sequence

from tqdm import tqdm

from songrecsys import ConfigMgr, LyricsGenius, PlaylistMgr, SpotifyWrapper, save_to_json, DEFAULT_PATH_PLAYLISTS

if __name__ == "__main__":
    config = ConfigMgr()
    sp = SpotifyWrapper(config, "spotify")
    pl = PlaylistMgr(spotify_api=sp)
    songs = pl.get_all_playlists_and_tracks(save=True, load_saved=True, max_playlist_count=50)
    pl.summary(songs)

    gs = LyricsGenius(config) 
    songs = gs.add_lyrics_to_dataset(songs)
    save_to_json(songs, DEFAULT_PATH_PLAYLISTS)
    
