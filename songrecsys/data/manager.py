import json
import pickle
from enum import Enum, auto
from pathlib import Path
from typing import Dict, NoReturn, Text

from pandas import DataFrame

from songrecsys.consts import (DEFAULT_PATH_DATA_DIR, DEFAULT_PATH_MERGED_DATA,
                               DEFAULT_PATH_PLAYLISTS, DEFAULT_PATH_TRACKS,
                               DEFAULT_PATH_TRACKS_LYRICS)
from songrecsys.schemes.mergeddata import MergedData
from songrecsys.schemes.playlist import Playlist
from songrecsys.schemes.track import Track
from songrecsys.utils.utils import override_prompt


def mapper(playlists=None,
           tracks=None,
           merged_data=None,
           lyrics=None):
    if playlists:
        playlists = playlists, DEFAULT_PATH_PLAYLISTS, 'playlists', Playlist
    if tracks:
        tracks = tracks, DEFAULT_PATH_TRACKS, 'tracks', Track
    if merged_data:
        merged_data = merged_data, DEFAULT_PATH_MERGED_DATA, 'merged_data', None
    if lyrics:
        lyrics = lyrics, DEFAULT_PATH_TRACKS_LYRICS, 'lyrics', None

    return playlists, tracks, merged_data, lyrics


def save_to_pickle(what: object,
                   where: Path,
                   default_override: bool = True) -> object:
    if override_prompt(default_override, where):
        with open(where, 'wb') as fhd:
            pickle.dump(what, fhd)
    return what


def load_from_pickle(where: Path):
    with open(where, 'rb') as fhd:
        return pickle.load(fhd)


def save_to_json(what: object,
                 where: Path,
                 default_override: bool = True) -> object:
    if override_prompt(default_override, f'{what}.json'):
        with open(f'{where}.json', 'w') as fhd:
            json.dump(what, fhd, indent=4, default=lambda obj: obj.__dict__)
    return what


def load_from_json(where: Path) -> object:
    with open(f'{where}.json', 'r') as fhd:
        return json.load(fhd)


class DataFormat:
    json = auto()
    pickle = auto()

    saver = {json: save_to_json,
             pickle: save_to_pickle}
    loader = {json: load_from_json,
              pickle: load_from_pickle}


def dump(playlists=None,
         tracks=None,
         merged_data=None,
         lyrics=None,
         data_format: DataFormat = DataFormat.json,
         default_override: bool = True) -> NoReturn:
    saver = DataFormat.saver.get(data_format)
    for data, path, _, _ in filter(None, mapper(playlists,
                                                tracks,
                                                merged_data,
                                                lyrics)):
        saver(data, path, default_override)


def load(playlists=None,
         tracks=None,
         merged_data=None,
         lyrics=None,
         data_format: DataFormat = DataFormat.json):
    return_value = {}
    loader = DataFormat.loader.get(data_format)
    for _, path, name, base_class in filter(None, mapper(playlists,
                                                         tracks,
                                                         merged_data,
                                                         lyrics)):
        try:
            print(f'Loading {name} from {path}', end='... ')
            if base_class:
                return_value[name] = {k: base_class(**v) for k, v in loader(path).items()}
            else:
                return_value[name] = loader(path)
            print('OK')
        except Exception as e:
            print(f'FAILED: {e}')
    return return_value


def save_to_csv(playlists=None, tracks=None):
    for data, path, _ in filter(None, mapper(playlists, tracks)):
        df = (DataFrame
              .from_dict({k: v.__dict__ for k, v in data.items()},
                         orient='index')
              .reset_index())
        df.to_csv(f'{path}.csv', index=False)
