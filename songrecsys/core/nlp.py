from os.path import dirname, exists, join
from typing import Text

from pymagnitude import Magnitude, MagnitudeUtils

from songrecsys.consts import DEFAULT_PATH_LANG_MODELS_DIR
from songrecsys.schemes import ModelPath


class NLP(Magnitude):
    def __init__(self, model_path: ModelPath):
        self._model_path = model_path

        model_local_path = join(dirname(__file__), '..', 'data', 'models', self._model_path)
        use_stream = not exists(model_local_path)

        if use_stream:
            print(f'{self._model_path} will be used in streamed mode')
        else:
            self._model_path = model_local_path
            print(f'{model_local_path} will be used locally')
        try:
            super().__init__(self._model_path, stream=use_stream, log=True)
        except RuntimeError:
            print(f'Cannot initialize with stream mode: {use_stream}.',
                  f'Trying to download model to {DEFAULT_PATH_LANG_MODELS_DIR}')
            MagnitudeUtils.download_model(self._model_path,
                                          download_dir=DEFAULT_PATH_LANG_MODELS_DIR,
                                          log=True)
