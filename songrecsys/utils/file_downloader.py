from pathlib import Path
from typing import NoReturn, Text

import requests

from songrecsys.utils.utils import tqdm


def download_file(url: Text, filename: Text = False, verbose: bool = False) -> NoReturn:
    if not filename:
        local_filename = Path('.') / url.split('/')[-1]
    else:
        local_filename = filename
    r = requests.get(url, stream=True)
    file_size = int(r.headers['Content-Length'])
    chunk = 1
    chunk_size = 1024
    num_bars = int(file_size / chunk_size)

    if verbose:
        print(dict(file_size=file_size))
        print(dict(num_bars=num_bars))

    with open(local_filename, 'wb') as fp:
        for chunk in tqdm(r.iter_content(chunk_size=chunk_size), total=num_bars, unit='KB', desc=local_filename, leave=True):
            fp.write(chunk)
    return
