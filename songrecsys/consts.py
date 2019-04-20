import json
from enum import Enum
from pathlib import Path
from typing import NewType, Text

DEFAULT_PATH_CONFIG = 'config.json'
DEFAULT_PATH_DATA_DIR = Path('data')
DEFAULT_PATH_MERGED_DATA = DEFAULT_PATH_DATA_DIR / 'data.json'
DEFAULT_PATH_PLAYLISTS = DEFAULT_PATH_DATA_DIR / 'playlists.json'
DEFAULT_PATH_TRACKS = DEFAULT_PATH_DATA_DIR / 'tracks.json'
DEFAULT_PATH_LANG_MODELS_DIR = DEFAULT_PATH_DATA_DIR / 'models'
