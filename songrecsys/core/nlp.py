from pymagnitude import Magnitude, MagnitudeUtils

from songrecsys.consts import DEFAULT_PATH_LANG_MODELS_DIR
from songrecsys.schemes import ModelPath


class NLP(Magnitude):

    def __init__(self, model_path: ModelPath, use_stream: bool = False):
        self._model_path = model_path
        model = MagnitudeUtils.download_model(str(self._model_path.concatenated_info), download_dir=str(DEFAULT_PATH_LANG_MODELS_DIR), log=True)

        super().__init__(model, stream=use_stream)
