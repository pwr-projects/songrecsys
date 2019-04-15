from .consts import *
from .config import *
from .spotify import *
from .lyrics import *
from .utils import *
from .core import *
from .schemes import *

import os
if not os.path.exists(DEFAULT_PATH_TMP_DIR):
    os.mkdir(DEFAULT_PATH_TMP_DIR)
