from enum import Enum
from pathlib import Path
from typing import NewType, Text

ModelPath = NewType('Model', Text)


class MAG:

    class weight(Enum):
        # WEIGHT
        light = 'light'
        medium = 'medium'
        heavy = 'heavy'

    class algorithm:
        glove = 'glove'
        ft = 'fasttext'
        w2v = 'word2vec'

    class corpus:
        # CORPUS
        GOOGLE_NEWS = lambda _: (MAG.algorithm.w2v, 'GoogleNews-vectors-negative300', [])
        WIKIPEDIA = lambda dim: (MAG.algorithm.glove, f'glove.6B.{dim}d', [50, 100, 200, 300])
        WIKIPEDIA_LEMMA = lambda dim: (MAG.algorithm.glove, f'glove-lemmatized.6B.{dim}d', [50, 100, 200, 300])
        COMMON_CRAWL_GL = lambda _: (MAG.algorithm.glove, 'glove.840B.300d', [])
        TWITTER = lambda dim: (MAG.algorithm.glove, f'glove.twitter.27B.{dim}d', [25, 50, 100, 200])
        WIKI_NEWS = lambda _: (MAG.algorithm.ft, 'wiki-news-300d-1M', [])
        WIKI_NEWS_SUBWORD = lambda _: (MAG.algorithm.ft, 'wiki-news-300d-1M-subword', [])
        COMMON_CRAWL_FT = lambda _: (MAG.algorithm.ft, 'crawl-300d-2M', [])

    def __init__(self,
                 corpus: corpus,
                 weight: weight,
                 dimension: int = None):
        self.corpus = corpus
        self.weight = weight
        self.dimension = dimension

    @property
    def concatenated_info(self):
        return MAG.concat_info(self.corpus, self.weight, self.dimension)

    @staticmethod
    def concat_info(corpus: corpus,
                    weight: weight,
                    dimensions: int = None):
        algo, name, _ = corpus(dimensions)
        return Path(algo) / weight.value / name

    @staticmethod
    def get(corpus: corpus,
            weight: weight,
            dimensions: int = None) -> ModelPath:
        algo, name, poss_dims = corpus(dimensions)

        if poss_dims:
            poss_dims_str = ', '.join(map(str, poss_dims))
            assert (dimensions in poss_dims,
                    f'{dimensions} not available for {name}. Possible are: {poss_dims_str}')

        return Path() / algo / (name + '.magnitude')

    def __call__(self) -> ModelPath:
        return MAG.get(self.corpus,
                       self.weight,
                       self.dimension)
