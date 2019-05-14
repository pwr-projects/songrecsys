import re
from string import punctuation

__all__ = ['preprocess_lyrics', 'preprocess_title']


def remove_section_tags(lyrics: str):
    return re.sub(r'\[.*\]', '', lyrics)


def remove_brackets(lyrics: str):
    return re.sub(r'\(|\)', '', lyrics)


def preprocess_lyrics(lyrics: str):
    stages = (remove_section_tags, remove_brackets)

    for stage in stages:
        lyrics = stage(lyrics)

    return lyrics


def preprocess_title(title: str):
    title = re.sub(r"\(.*\)|\[.*\]", '', title)  # (feat.) [extended cut]
    title = re.sub(r"-.*", '', title)  # - Remastered ...
    # title = re.sub('|'.join(punctuation), '', title)
    return title
