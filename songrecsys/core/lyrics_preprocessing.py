import re


def remove_section_tags(lyrics: str) -> str:
    return re.sub(r'\[.*\]', '', lyrics)


def remove_brackets(lyrics: str) -> str:
    return re.sub(r'\(|\)', '', lyrics)


def preprocess_lyrics(lyrics: str) -> str:
    stages = (remove_section_tags, remove_brackets)

    for stage in stages:
        lyrics = stage(lyrics)

    return lyrics
