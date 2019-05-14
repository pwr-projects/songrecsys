from typing import *

from gensim.models import KeyedVectors, Word2Vec
from gensim.models.callbacks import CallbackAny2Vec
from torch import nn

from songrecsys.consts import *
from songrecsys.misc import *

__all__ = ['SongEmbedding']


class SongEmbedding(nn.Module):

    def __init__(self):
        super(SongEmbedding, self).__init__()
