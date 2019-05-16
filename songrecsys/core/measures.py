from typing import *
from warnings import warn

__all__ = ['Meas']


class Meas:

    @staticmethod
    def _check_type(args) -> NoReturn:
        assert all([isinstance(col, set) for col in args])

    @staticmethod
    def TP(true: Set[Any], preds: Set[Any]) -> int:
        Meas._check_type(locals().values())
        return len(true & preds)

    @staticmethod
    def FP(true: Set[Any], preds: Set[Any]) -> int:
        Meas._check_type(locals().values())
        return len(preds - true)

    @staticmethod
    def TN(true: Set[Any], preds: Set[Any]) -> int:
        Meas._check_type(locals().values())
        warn('TN is always 1 through to recommendation case.')
        return 1

    @staticmethod
    def FN(true: Set[Any], preds: Set[Any]) -> int:
        Meas._check_type(locals().values())
        warn('FN is always 0 through to recommendation case.')
        return 0

    @staticmethod
    def acc(true: Collection[Any], preds: Collection[Any]) -> float:
        true, preds = set(true), set(preds)
        return Meas.TP(true, preds) / len(preds)

    @staticmethod
    def prec(true: Collection[Any], preds: Collection[Any]) -> float:
        true, preds = set(true), set(preds)
        return Meas.TP(true, preds) / (Meas.TP(true, preds) + Meas.FP(true, preds))
