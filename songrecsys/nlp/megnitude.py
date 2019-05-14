from pymagnitude import Magnitude, MagnitudeUtils

from songrecsys.consts import *
from songrecsys.schemes import *

__all__ = ['NLP']


class NLP(Magnitude):

    def __init__(self, model_path, use_stream=False):
        self._model_path = model_path
        model = MagnitudeUtils.download_model(str(self._model_path.concatenated_info),
                                              download_dir=str(DIR_MAGNITUDE_MODELS),
                                              log=True)

        super().__init__(model, stream=use_stream)
