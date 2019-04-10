from os.path import exists, join, dirname
from typing import Text

from pymagnitude import *

from songrecsys.consts import ModelPath


class NLP:
    def __init__(self, model_path: ModelPath):
        self._model_path = model_path
        self._model = self._load_model()

    def _load_model(self) -> Magnitude:
        model_local_path = join(dirname(__file__), '..', 'models', self._model_path)
        use_stream = not exists(model_local_path)
        if use_stream:
            print( f'{self._model_path} will be used in streamed mode' )
        else:
            self._model_path = model_local_path
            print( f'{model_local_path} will be used locally' )

        return Magnitude(self._model_path, stream=use_stream, log=True)
