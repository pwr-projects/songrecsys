from enum import Enum, auto
from typing import *

NGramGenType = Generator[Iterable[Iterable[Union[Iterable[str], str]]], None, None]


class NGramType(Enum):
    BACKWARD = auto()
    FORWARD = auto()
    BACKWARD_AND_FORWARD = auto()


class NGram:

    def __init__(self, data: List[Any], n: int, ngram_type: NGramType = NGramType.BACKWARD_AND_FORWARD):
        self.data = data
        self.n = n
        if ngram_type != NGramType.BACKWARD_AND_FORWARD:
            assert self.n < len(self.data), '`n` has to be smaller than `data` length'
        else:
            assert len(self.data) > self.n * 2, '`n * 2 + 1` has to be greater than `data` length'
        self.ngram_type = ngram_type

    def __iter__(self) -> NGramGenType:
        return {
            NGramType.BACKWARD.value: self._gen_backward,
            NGramType.FORWARD.value: self._gen_forward,
            NGramType.BACKWARD_AND_FORWARD.value: self._gen_backward_and_forward
        }.get(self.ngram_type.value, self._gen_backward_and_forward)()

    def _gen_backward(self) -> NGramGenType:
        for idx in range(len(self.data) - self.n):
            yield [self.data[idx + n] for n in range(self.n)], self.data[idx + self.n]

    def _gen_forward(self) -> NGramGenType:
        for idx in range(len(self.data) - self.n):
            yield [[self.data[idx + n + 1] for n in range(self.n)], self.data[idx]]

    def _gen_backward_and_forward(self) -> NGramGenType:
        for idx in range(self.n, len(self.data) - self.n):
            back = [self.data[n] for n in range(idx - self.n, idx)]
            far = [self.data[n] for n in range(idx + 1, idx + self.n + 1)]
            yield [[*back, *far], self.data[idx]]
