from os.path import dirname, exists, join
from typing import Text

from pymagnitude import Magnitude, MagnitudeUtils

from songrecsys.consts import DEFAULT_PATH_LANG_MODELS_DIR
from songrecsys.schemes import ModelPath


class NLP(Magnitude):
    def __init__(self,
                 model_path,
                 force_download: bool = False):
        self._model_path = model_path

        model_local_path = DEFAULT_PATH_LANG_MODELS_DIR / self._model_path()
        use_stream = not model_local_path.exists

        if use_stream or force_download:
            self._model_path = self._model_path.concatenated_info
            print(f'{self._model_path} will be used in streamed mode')
        else:
            self._model_path = model_local_path
            print(f'{model_local_path} will be used locally')
            
        try:
            super().__init__(str(self._model_path), stream=use_stream, log=True)
        except:
            print(f'Cannot initialize with stream mode: {use_stream}.',
                  f'Trying to download model to {DEFAULT_PATH_LANG_MODELS_DIR}')
            MagnitudeUtils.download_model(str(self._model_path),
                                          download_dir=DEFAULT_PATH_LANG_MODELS_DIR,
                                          log=True)
