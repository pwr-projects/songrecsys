import os

from .config import *
from .consts import *
from .core import *
from .data import *
from .lyrics import *
from .multiprocessing import *
from .nlp import *
from .schemes import *
from .spotify import *
from .utils import *

for dir_name in (DIR_DATA_ROOT, DIR_MAGNITUDE_MODELS, DIR_W2V_MODELS):
    dir_name.mkdir(exist_ok=True)
