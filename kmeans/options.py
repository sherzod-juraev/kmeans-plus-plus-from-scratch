from enum import Enum


class NormalizationOptions(str, Enum):

    Z_SCORE = 'z-score'
    MIN_MAX = 'minmax'

class KmeansInitOptions(str, Enum):

    KMEANS_PP = 'kmeans_pp'
    RANDOM = 'random'