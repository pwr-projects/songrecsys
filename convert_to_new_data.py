from songrecsys import (load_from_json, load_from_pickle, save_to_json,
                        save_to_pickle)
from songrecsys.consts import (DEFAULT_PATH_PLAYLISTS, DEFAULT_PATH_TRACKS,
                               DEFAULT_PATH_TRACKS_LYRICS)
from songrecsys.schemes.data import Data, Playlist, Track
from songrecsys.utils import tqdm

data = Data()
playlists = load_from_pickle(DEFAULT_PATH_PLAYLISTS, verbose=True)
for playlist_id, item in tqdm(playlists.items(), 'Converting playlists'):
    new_playlist = Playlist(id=playlist_id, name=item.name, tracks=item.tracks)
    data.playlists['spotify'].append(new_playlist)
del playlists

lyrics = load_from_pickle(DEFAULT_PATH_TRACKS_LYRICS, verbose=True)
tracks = load_from_pickle(DEFAULT_PATH_TRACKS, verbose=True)

for track_id, track in tqdm(tracks.items(), 'Converting tracks'):
    new_track = Track(track.title, track.artists, lyrics[track_id])
    data.tracks[track_id] = new_track

del lyrics
del tracks

save_to_json(data, 'data/data')
save_to_pickle(data, 'data/data')
