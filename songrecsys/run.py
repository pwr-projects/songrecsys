import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
auth_mgr = SpotifyClientCredentials(client_id='8fff6a62213b468989c81fa6146af493',
                                    client_secret='1563924c566941d08ad01de17ce8a61e')

spotify = spotipy.Spotify(client_credentials_manager=auth_mgr)

results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])
