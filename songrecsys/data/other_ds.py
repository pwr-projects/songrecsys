import csv
import re
from pathlib import Path
from typing import AnyStr, Iterable, NoReturn, Optional, Union

import pandas as pd

from songrecsys.consts import *
from songrecsys.misc import tqdm, wc


class OtherDS:

    def __init__(self):
        self._data: Optional[Iterable[Iterable[str]]] = None

    def load(self) -> Optional[pd.DataFrame]:
        if not FILEPATH_DATASET.exists():
            return None
            
        self._data = []
        with open(FILEPATH_DATASET) as fhd:
            reader = csv.reader(fhd, delimiter=';', quotechar='|', quoting=csv.QUOTE_ALL)
            for row in tqdm(reader, f'Loading dataset from {FILEPATH_DATASET}', leave=False,
                            total=wc(FILEPATH_DATASET)):
                self._data.append([txt.strip() for txt in row])
        return self._data

    def clean_dataset(self) -> NoReturn:
        if FILEPATH_DATASET.exists():
            return

        data: Iterable[Iterable[str]] = []
        with open(FILEPATH_RAW_DATASET) as fhd_in:
            reader = csv.reader(fhd_in, delimiter=',', quotechar='"')
            with open(FILEPATH_DATASET, 'w') as fhd_out:
                writer = csv.writer(fhd_out, delimiter=';', quotechar='|', quoting=csv.QUOTE_ALL)
                for row in tqdm(reader, 'Reading dataset', wc(FILEPATH_RAW_DATASET)):
                    row = [txt.strip().replace('"', '') for txt in row]
                    writer.writerow(row)
