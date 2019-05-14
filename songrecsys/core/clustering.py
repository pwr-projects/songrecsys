from typing import *

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans

from songrecsys.schemes import *

__all__ = ['Clustering']


class Clustering:

    def __init__(self, data: Data):
        self._data = data
        self._plot_data = AudioFeatures.to_df(self._data)

    def fit(self, **kwargs) -> KMeans:
        kmeans = KMeans(random_state=0, **kwargs).fit(self._plot_data)
        return kmeans

    def scatter_matrix(self) -> plt.figure:
        plot = sns.pairplot(self._plot_data, plot_kws=dict(s=20))
        plt.title('Scatter matrix')
        plot.savefig("output.png", dpi=600)
        return plot
