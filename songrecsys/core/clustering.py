from typing import *

from sklearn.cluster import KMeans

from songrecsys.schemes import *

__all__ = ['Clustering']

class Clustering: 

    def __init__(self, data: Data):
        self._data = data

    def simple_preprocessing(self) -> Iterable[Iterable[Union[float, int]]]:
        return [track.audio_features.to_list() for track in self._data.tracks.values() if track.audio_features]

    def fit(self, preprocessing: Callable):
        data = preprocessing(self)
        kmeans = KMeans(n_clusters=2, random_state=0).fit(data)
        print(kmeans.labels_)
