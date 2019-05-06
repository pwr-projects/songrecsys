import os

from .config import *
from .consts import *
from .core import *
from .data import *
from .lyrics import *
from .nlp import *
from .schemes import *
from .spotify import *
from .utils import *

for dir_name in (DEFAULT_PATH_DATA_DIR, DEFAULT_PATH_LANG_MODELS_DIR):
    dir_name.mkdir(exist_ok=True)
