from time import sleep
from typing import Dict, List, Iterable

from songrecsys.nlp.text_preprocessing import preprocess_title
from songrecsys.schemes import Artist, Playlist, Track


def mp_artist_extractor(args) -> Artist:
    sp, artist_id = args
    # stdout.write(f'Downloading artist: {artist_id}\n')
    # stdout.flush()
    not_downloaded = True
    while not_downloaded:
        try:
            artist = Artist.download_info_about_artist(sp, artist_id)
            not_downloaded = False
        except Exception as e:
            # stdout.write(f'Retrying to download artist: {artist_id}\n')
            # stdout.flush()
            print(e)
            sleep(2)
    return artist


def mp_extract_artist_song_pair(args) -> List[str]:
    playlist, artists, tracks = args
    tracks: List[Track] = list(map(tracks.get, playlist.tracks))
    all_tracks: List[str] = list()
    for track in tracks:
        artists_names: Iterable = list(
            filter(
                None,
                map(
                    lambda artist_id: artists.get(artist_id).name.lower() if artists.get(artist_id) else None,
                    track.artists_ids,
                )))
        all_tracks.append(" ".join([*artists_names, preprocess_title(track.title.lower())]))
    all_tracks.append(' ')
    return all_tracks
