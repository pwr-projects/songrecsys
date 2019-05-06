from sys import stdout
from time import sleep

from songrecsys.schemes import Track


def mp_lyrics_downloader(track: Track, getter):
    artists = ', '.join(track.artists)
    what = f'{artists} - {track.title}'
    # stdout.write(f'Downloading {what}\n')

    stdout.flush()
    got = False
    while not got:
        try:
            track.lyrics = getter(track.title.replace('(', '').replace(')', ''), ' '.join(track.artists))
            got = True
        except:
            sleep(2)
    if track.lyrics:
        stdout.write(f'Downloaded  {what}\n')
        stdout.flush()
