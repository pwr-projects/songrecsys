# songrecsys
Song recommendation system

## Data structure
```json
{
    "playlists": {
        "{username: str}": [
            {
                "id": "{playlist_id: str}",
                "name" : "{name: str}",
                "tracks": [
                    "{track_id: str}",
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
            "artists_ids": [
                "{artist_id: str}",
                ...
            ],
            "lyrics": "{lyrics: str}",
        },
        ...
    },
    "artists": {
        "{artist_id: str}": {
            "name": "{name: str}",
            "albums_id": [
                "{album_id: str}",
                ...
            ],
            ...
        },
        ...
    },
    "albums": {
        "{album_id: str}": {
            "artists_id": [
                "{artist_id: str}",
                ...
            ],
            "name": "{name: str}",
            "tracks": [
                "{track_id: str}",
                ...
            ],
        },
        ...
    }
}
```