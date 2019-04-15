import json
from enum import Enum
from os.path import join
from typing import NewType, Text

DEFAULT_PATH_CONFIG = 'config.json'
DEFAULT_PATH_DATA_DIR = 'data'
DEFAULT_PATH_MERGED_DATA = join(DEFAULT_PATH_DATA_DIR, 'data.json')
DEFAULT_PATH_PLAYLISTS = join(DEFAULT_PATH_DATA_DIR, 'playlists.json')
DEFAULT_PATH_TRACKS = join(DEFAULT_PATH_DATA_DIR, 'tracks.json')
DEFAULT_PATH_LANG_MODELS_DIR = join(DEFAULT_PATH_DATA_DIR, 'models')
