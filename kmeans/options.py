from enum import Enum


class NormalizationOptions(str, Enum):

    Z_SCORE = 'z-score'
    MIN_MAX = 'minmax'