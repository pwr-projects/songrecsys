from sys import stdout
from time import sleep

from songrecsys.schemes import Track
from songrecsys.nlp import preprocess_title

def mp_lyrics_downloader(id: str, track: Track, artists,  getter):
    what = f'{artists} - {track.title}'
    # stdout.write(f'Downloading {what}\n')

    stdout.flush()
    got = False
    while not got:
        try:
            track.lyrics = getter(preprocess_title(track.title), ' '.join(artists))
            got = True
        except:
            sleep(2)
    if track.lyrics:
        stdout.write(f'Downloaded  {what}\n')
        stdout.flush()
    return id, track