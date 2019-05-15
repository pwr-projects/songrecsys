from typing import *

from gensim.models import KeyedVectors, Word2Vec
from gensim.models.callbacks import CallbackAny2Vec
from keras.layers import Embedding, Input, Reshape
from keras.models import Model

from songrecsys.consts import *
from songrecsys.misc import *
from songrecsys.schemes import *

__all__ = ['SongEmbedding']


class SongEmbedding:

    def __init__(self, data: Data, emb_size: int = 15):

        self.emb_size = emb_size
        self.data = data
        self.model = self.init_model()

    def init_model(self) -> Model:

        audio = Input(name='audio', shape=[1])

        audio_emb = Embedding(name='audio embedding', input_dim=len(self.data.tracks), output_dim=self.emb_size)(audio)

        merged = Reshape(target_sape=[1])(audio_emb)

        model = Model(inputs=audio, outputs=merged)
        model.compile(optimizer='Adam', loss='mse')

        return model
