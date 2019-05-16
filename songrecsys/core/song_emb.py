from __future__ import annotations

from multiprocessing import cpu_count
from typing import *

from gensim.models import Word2Vec
from gensim.models.keyedvectors import Word2VecKeyedVectors
from gensim.utils import RULE_KEEP

from songrecsys.consts import *
from songrecsys.misc import *
from songrecsys.schemes import Data

__all__ = ['SongEmb']


class SongEmb:

    def __init__(self, data: Data, epochs: int = 200, emb_size: int = 300, window: int = 10,
                 workers: int = cpu_count()):
        self.data = data
        self.workers = workers
        self.epochs, self.emb_size, self.window = epochs, emb_size, window
        self.model_path = FILEPATH_W2V_MODEL(self.epochs, self.emb_size, self.window)

    def _extract_data(self) -> List[List[str]]:
        return [list(filter(None, pl.tracks)) for pl in self.data.playlists.values() if pl.tracks]

    def train(self) -> Word2VecKeyedVectors:
        learner_info = LearnerInfo(self.epochs, self.emb_size, self.window)

        data = self._extract_data()
        model = Word2Vec(size=self.emb_size, window=self.window, workers=self.workers)
        model.build_vocab(data, trim_rule=lambda *_: RULE_KEEP)
        model.train(data, epochs=self.epochs, total_examples=len(data), callbacks=[learner_info])
        model.wv.save(str(self.model_path))
        return model.wv

    def get_model(self) -> Word2VecKeyedVectors:
        if self.model_path.exists():
            return Word2VecKeyedVectors.load(str(self.model_path))
        return self.train()
