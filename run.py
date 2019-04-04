#!.env/bin/python
import json
from pprint import pprint
from typing import Dict, Sequence

from tqdm import tqdm

from songrecsys import ConfigMgr, LyricsGenius, SpotifyWrapper

if __name__ == "__main__":
    config = ConfigMgr()
    sp = SpotifyWrapper(config, "spotify")
    songs = sp.pl.get_all_playlists_and_tracks(save=False, load_saved=False)

    # genius = LyricsGenius(config)
    # lyrics = genius.lyrics("Renaissance", "Marcus Miller")
