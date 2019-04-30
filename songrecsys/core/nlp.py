from os.path import dirname, exists, join
from typing import Text

from pymagnitude import Magnitude, MagnitudeUtils

from songrecsys.consts import DEFAULT_PATH_LANG_MODELS_DIR
from songrecsys.schemes import ModelPath


class NLP(Magnitude):
    def __init__(self,
                 model_path,
                 use_stream: bool = False):
        self._model_path = model_path
        super().__init__(MagnitudeUtils.download_model(str(self._model_path.concatenated_info),
                                                       download_dir=str(DEFAULT_PATH_LANG_MODELS_DIR),
                                                       log=True),
                         stream=use_stream)
