from sys import stdout
from time import sleep

from songrecsys.nlp import *
from songrecsys.schemes import *

__all__ = ['mp_lyrics_downloader']


def mp_lyrics_downloader(id: str, track: Track, artists, getter):
    what = f'{artists} - {track.title}'

    stdout.flush()
    got = False
    while not got:
        try:
            track.lyrics = getter(preprocess_title(track.title), artists[0] if len(artists) > 0 else '')
            got = True
        except Exception as e:
            print(e)
            sleep(2)
    if track.lyrics:
        stdout.write(f'Downloaded  {what}\n')
        stdout.flush()
    return id, track
