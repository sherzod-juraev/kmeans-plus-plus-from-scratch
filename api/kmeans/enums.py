from enum import Enum


class KmeansInit(str, Enum):

    kmeans_pp = 'kmeans++'
    random = 'random'


class Normalization(str, Enum):

    z_score = 'z_score'
    minmax = 'minmax'