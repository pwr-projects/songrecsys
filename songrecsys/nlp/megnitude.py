from pymagnitude import Magnitude, MagnitudeUtils

from songrecsys.consts import *
from songrecsys.schemes import ModelPath


class NLP(Magnitude):

    def __init__(self, model_path: ModelPath, use_stream: bool = False):
        self._model_path = model_path
        model = MagnitudeUtils.download_model(str(self._model_path.concatenated_info),
                                              download_dir=str(DIR_MODELS),
                                              log=True)

        super().__init__(model, stream=use_stream)
