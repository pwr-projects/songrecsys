from torch import *

__all__ = ['Model']


class Model:

    def __init__(self):
        self._model = lstm(15)
