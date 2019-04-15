import json
from os.path import exists
from typing import Dict, NoReturn, Text

from songrecsys.consts import (DEFAULT_PATH_MERGED_DATA,
                               DEFAULT_PATH_PLAYLISTS, DEFAULT_PATH_TRACKS)
from songrecsys.schemes.mergeddata import MergedData
from songrecsys.schemes.playlist import Playlist
from songrecsys.schemes.track import Track


def save_to_json(obj: object,
                 where: Text,
                 default_override: bool = True) -> object:
    override = True
    if not default_override and exists(where):
        answer = input(f'{where} exists. Override? [Yy/Nn] ')
        override = answer in 'YyTt'

    if override:
        with open(where, 'w') as fhd:
            json.dump(obj, fhd, indent=4, default=lambda obj: obj.__dict__)

    return obj


def load_from_json(where: Text) -> object:
    with open(where, 'r') as fhd:
        return json.load(fhd)


def dump(playlists: Dict[Text, Playlist] = None,
         tracks: Dict[Text, Track] = None,
         merged_data: MergedData = None,
         verbose: bool = True) -> NoReturn:
    if playlists:
        if verbose:
            print(f'Saving playlists to {DEFAULT_PATH_PLAYLISTS}', end='... ')
        save_to_json(playlists, DEFAULT_PATH_PLAYLISTS)
        if verbose:
            print('OK')
    if tracks:
        if verbose:
            print(f'Saving tracks to {DEFAULT_PATH_TRACKS}', end='... ')
        save_to_json(tracks, DEFAULT_PATH_TRACKS)
        if verbose:
            print('OK')
    if merged_data:
        if verbose:
            print(f'Saving merged data to {DEFAULT_PATH_MERGED_DATA}', end='... ')
        save_to_json(merged_data, DEFAULT_PATH_MERGED_DATA)
        if verbose:
            print('OK')


def load(playlists: bool = False,
         tracks: bool = False,
         merged_data: bool = False) -> Dict[Text, object]:
    return_value = {}
    
    if playlists:
        try:
            print(f'Loading playlists from {DEFAULT_PATH_PLAYLISTS}', end='... ')
            return_value['playlists'] = load_from_json(DEFAULT_PATH_PLAYLISTS)
            print('OK')
        except:
            print('FAILED')
    if tracks:
        try:
            print(f'Loading tracks from {DEFAULT_PATH_TRACKS}', end='... ')
            return_value['tracks'] = load_from_json(DEFAULT_PATH_TRACKS)
            print('OK')
        except:
            print('FAILED')
    if merged_data:
        try:
            print(f'Loading merged data from {DEFAULT_PATH_MERGED_DATA}', end='... ')
            return_value['merged_data'] = load_from_json(DEFAULT_PATH_MERGED_DATA)
            print('OK')
        except:
            print('FAILED')
    return return_value
