#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# skgmm.py - Файл містить засоби для роботи із кривими Гаусса

import operator
import numpy as np
from sklearn.mixture import GMM  # GaussianMixture as GMM


# Підрахунок середнього значення коефіцієнтів
def gmm_score(gmm, x):
    return np.sum(gmm.score(x))


# Клас для роботи з кривими Гаусса
class GMMSet(object):
    def __init__(self, gmm_order=32):
        self.gmms = []
        self.gmm_order = gmm_order
        self.y = []

	# Додаємо дані нового голосу
    def fit_new(self, x, label):
        self.y.append(label)
        gmm = GMM(n_components=self.gmm_order)
        gmm.fit(x)
        self.gmms.append(gmm)

    def before_pickle(self):
        pass

    def after_pickle(self):
        pass

	# Із існуючих кривих знаходимо найбільш схожу до форми вхідного сигналу
    def predict_one(self, x):
        scores = [gmm_score(gmm, x) / len(x) for gmm in self.gmms]
        p = sorted(enumerate(scores), key=operator.itemgetter(1), reverse=True)
        p = [(str(self.y[i]), y, p[0][1] - y) for i, y in p]
        result = [(self.y[index], value) for (index, value) in enumerate(scores)]
        p = max(result, key=operator.itemgetter(1))
        return p[0]
