from .consts import *
from .config import *
from .spotify import *
from .lyrics import *
from .utils import *
from .core import *
from .schemes import *
from .data import *

import os
for dir_name in (DEFAULT_PATH_DATA_DIR,
                 DEFAULT_PATH_LANG_MODELS_DIR):
    dir_name.mkdir(exist_ok=True)