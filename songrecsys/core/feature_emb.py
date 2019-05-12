from typing import *

from gensim.models import KeyedVectors, Word2Vec
from gensim.models.callbacks import CallbackAny2Vec

from songrecsys.consts import *
from songrecsys.misc import *

__all__ = ['AudioModel', 'LearnerInfo']


class AudioModel:

    def __init__(self, size: int = 15):
        self._size = size

    def _init_model(self):
        ...

    def train(self, data: Iterable[Any]):
        ...


class LearnerInfo(CallbackAny2Vec):

    def __init__(self, epochs: int, size: int):
        self.epoch_bar = tqdm(desc="Epochs", total=epochs)
        self.batch_bar = tqdm(desc='Batch')
        self.size = size

    def on_epoch_end(self, model: Word2Vec) -> NoReturn:
        model.wv.save(str(FILEPATH_W2V_MODEL(self.epoch_bar.n, self.size)))
        self.epoch_bar.update()

    def on_batch_end(self, model: Word2Vec) -> NoReturn:
        self.batch_bar.update()
