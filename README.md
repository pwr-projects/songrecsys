# songrecsys
Song recommendation system

## Data structure
```json
{
    "playlists": {
        "{username: str}": [
            {
                "id": "{spotify_playlist_id: str}",
                "name" : "{name: str}",
                "tracks": [
                    "{spotify_track_id: str}",
                    ...
                ]
            },
            ...
        ]
    },
    "tracks": {
        "{spotify_track_id: str}": {
            "title": "{title: str}",
            "artists": [
                "{artist: str}",
                ...
            ],
            "lyrics": "{lyrics: str}",
        },
        ...
    }
}
```