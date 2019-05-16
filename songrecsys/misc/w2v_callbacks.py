from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec

from songrecsys.consts import *
from songrecsys.misc.utils import *

__all__ = ['LearnerInfo']


class LearnerInfo(CallbackAny2Vec):

    def __init__(self, epochs: int, size: int, window:int):
        DIR_W2V_MODELS.mkdir(exist_ok=True)
        self.epoch_bar = tqdm(desc="Epochs", total=epochs)
        self.batch_bar = tqdm(desc='Batch')
        self.size = size
        self.window = window

    def on_epoch_end(self, model: Word2Vec):
        self.epoch_bar.update()
        model.wv.save(str(FILEPATH_W2V_MODEL(self.epoch_bar.n, self.size, self.window)))

    def on_batch_end(self, model: Word2Vec):
        self.batch_bar.update()
