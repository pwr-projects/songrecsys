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
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
