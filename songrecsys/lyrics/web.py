# coding=utf-8
import re
import sys
from typing import *

import requests
from bs4 import BeautifulSoup

from songrecsys.config import *
from songrecsys.lyrics.lyrics_provider import *

try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus

__all__ = ['WebLyrics']


class WebLyrics(LyricsProvider):

    def __init__(self, config: ConfigBase):
        self.verbose = getattr(config, 'verbose', False)

    def get(self, title, artist) -> Optional[str]:

        search_name = f'{artist} {title} genius lyrics'
        name = quote_plus(search_name)
        url = f'http://www.google.com/search?q={name}'
        result = requests.get(url).text
        link_start = result.find('https://genius.com')
        if link_start == -1:
            print(f'Lyrics not found on genius:  {artist} - {title}')
            return None
        link_end = result.find('"', link_start + 1)
        link = result[link_start:link_end].lower()
        link = re.sub(r"&.*", '', link)
        link_correct = self._check_link_genius(artist, title, link)
        if not link_correct:
            print(f'Link not correct:            {artist} - {title}')
            return None

        lyrics_html = requests.get(link).text
        soup = BeautifulSoup(lyrics_html, 'lxml')
        raw_lyrics = str(soup.findAll('div', attrs={'class': 'lyrics'}))
        lyrics = raw_lyrics[1:len(raw_lyrics) - 1]
        lyrics = re.sub(r'<[^<>]*>', '', lyrics)
        if sys.version_info < (3, 0):
            lyrics = re.sub(r'\\n', '\n', lyrics)
        return lyrics[2:]

    @classmethod
    def _check_link_genius(cls, artist, title, link):
        songinfo = "%s %s" % (artist, title)
        songinfo = songinfo.lower()
        songinfo = re.sub(r"ö", "o", songinfo)
        songinfo = re.sub(r"ä", "a", songinfo)
        songinfo = re.sub(r"ü", "u", songinfo)
        songinfo = re.sub(r"[^a-zA-Z0-9 ]", '', songinfo)
        songinfo_array = songinfo.split()
        for item in songinfo_array:
            if link.find(item) == -1:
                return False
        return True
