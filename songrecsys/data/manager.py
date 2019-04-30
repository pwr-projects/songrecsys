import json
import pickle
from enum import auto
from pathlib import Path
from typing import Dict, NoReturn, Tuple

from pandas import DataFrame

from songrecsys.consts import (DEFAULT_PATH_MERGED_DATA,
                               DEFAULT_PATH_PLAYLISTS, DEFAULT_PATH_TRACKS,
                               DEFAULT_PATH_TRACKS_LYRICS)
from songrecsys.schemes.mergeddata import MergedData
from songrecsys.schemes.playlist import Playlist
from songrecsys.schemes.track import Track
from songrecsys.utils.utils import override_prompt, tqdm


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
    if override_prompt(default_override, f'{where}.json'):
        with open(f'{where}.json', 'w') as fhd:
            for chunk in tqdm(json.JSONEncoder(default=lambda obj: obj.__dict__).iterencode(what)):
                fhd.write(chunk + '\n')
        # with open(f'{where}.json', 'w') as fhd:
        #     json.dump(what, fhd, indent=4, default=lambda obj: obj.__dict__)
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
    for data, path, name, _ in filter(None, mapper(playlists,
                                                   tracks,
                                                   merged_data,
                                                   lyrics)):
        try:
            print(f'Saving {name} to {path}', end='...')
            saver(data, path, default_override)
            print('OK')
        except Exception as e:
            print(f'FAILED: {e}')


def merge_data(playlists: Dict,
               tracks: Dict,
               lyrics: Dict,
               save: bool = True) -> MergedData:
    merged_data = []

    for playlist_id, playlist in playlists.items():
        playlist = Playlist(id=playlist_id, **(playlist if isinstance(playlist, dict) else playlist.__dict__))
        new_tracks = [Track(id=tr, **{**(tracks[tr] if isinstance(tracks[tr], dict) else tracks[tr].__dict__),
                                      'lyrics': lyrics.get(tr)})
                      for tr in playlist.tracks if tr]
        playlist.tracks = new_tracks
        merged_data.append(playlist)

    if save:
        dump(merged_data=merged_data)

    return merged_data


def load(playlists=None,
         tracks=None,
         merged_data=None,
         lyrics=None,
         data_format: DataFormat = DataFormat.json):
    return_value = {}
    loader = DataFormat.loader.get(data_format)
    for _, path, name, base_class in filter(None, mapper(playlists,
                                                         tracks,
                                                         lyrics,
                                                         merged_data)):
        try:
            print(f'Loading {name} from {path}', end='... ')
            if base_class:
                return_value[name] = {k: base_class(**(v if isinstance(v, dict) else v.__dict__))
                                      for k, v in tqdm(loader(path).items(), 'Converting to objects')}
            else:
                return_value[name] = loader(path)
            print('OK')
        except Exception as e:
            print(f'FAILED: {e}')
    # if not return_value.get('merged_data') and return_value.get('playlists') and return_value.get('tracks') and return_value.get('lyrics'):
    #     return_value[name] = merge_data(return_value.get('playlists'),
    #                                     return_value.get('tracks'),
    #                                     return_value.get('lyrics'),
    #                                     save=False)
    return return_value


def split_merged_data(merged_data: MergedData,
                      save: bool = True) -> Tuple:
    playlists, tracks = {}, {}

    for pl in tqdm(merged_data, 'Spliting: playlists'):

        new_tracks = []
        for pl_tr in tqdm(pl.tracks, 'Spliting: tracks'):
            new_tracks.append(pl_tr.id)
            tracks[pl_tr.id] = Track(**pl_tr.__dict__, use_kwargs=False)

        new_playlist = Playlist(**pl.__dict__, use_kwargs=False)
        new_playlist.tracks = new_tracks
        playlists[pl.id] = new_playlist

    if save:
        dump(playlists=playlists, tracks=tracks)

    return playlists, tracks


def save_to_csv(playlists=None, tracks=None):
    for data, path, _ in filter(None, mapper(playlists, tracks)):
        df = (DataFrame
              .from_dict({k: v if isinstance(v, dict) else v.__dict__
                          for k, v in tqdm(data.items(), 'Converting to pandas DataFrame')},
                         orient='index')
              .reset_index())
        df.to_csv(f'{path}.csv', index=False)
