from typing import *

from keras import losses, metrics, optimizers
from keras.layers import (LSTM, Activation, Concatenate, Dense, Dropout, Embedding, Input)
from keras.models import Model

from songrecsys.consts import *
from songrecsys.misc import *
from songrecsys.schemes import Data

__all__ = ['AudioEmb']


class AudioEmb:

    def __init__(self, data: Data, emb_size: int = 300):

        self.emb_size = emb_size
        self.data = data
        self.model = self.init_model()

    def init_model(self) -> Model:
        emb_input = len(self.data.tracks)
        emb = Embedding(emb_input, self.emb_size, input_length=70, trainable=False)
        lstm = LSTM(self.emb_size, dropout=0.3, recurrent_dropout=0.3)(emb)
        audio_features = Input((1,))
        cont = Concatenate()(lstm, audio_features)
        drop = Dropout(0.6)(cont)
        dens = Dense(1)(drop)
        act_func = Activation('sigmoid')(dens)
        model = Model([emb, audio_features], act_func)
        model.compile(optimizers.Adam, losses.mean_squared_error, [metrics.acc])

        return model
