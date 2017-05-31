#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# interface.py - Файл для аналізу параметрів консолі

import time
import os
import sys
from collections import defaultdict
from scipy.io import wavfile
import numpy as np
import cPickle as pickle
import traceback as tb

from feature import mix_feature
from filters.VAD import VAD

try:
    from gmmset import GMMSetPyGMM as GMMSet
    from gmmset import GMM
except:
    print >> sys.stderr, "Warning: failed to import fast-gmm, use gmm from scikit-learn instead"
    from skgmm import GMMSet, GMM

CHECK_ACTIVE_INTERVAL = 1  # seconds


class ModelInterface(object):
    UBM_MODEL_FILE = 'model/ubm.mixture-32.utt-300.model'

    def __init__(self):
        self.features = defaultdict(list)
        self.gmmset = GMMSet()
        self.vad = VAD()

	# Ініціалізуємо VAD модуль
    def init_noise(self, fs, signal):
        self.vad.init_noise(fs, signal)

	# Викликаємо VAD модуль для фільтрації шумів
    def filter(self, fs, signal):
        ret, intervals = filter(fs, signal)
        orig_len = len(signal)

        if len(ret) > orig_len / 3:
            return ret
        return np.array([])

	# Додаємо сигнал до бази даних голоса даного диктора
    def enroll(self, name, fs, signal):
        feat = mix_feature((fs, signal))
        self.features[name].extend(feat)
		
	# Отримати базу даних коефіцієнтів всіх дикторів
    def _get_gmm_set(self):
        if os.path.isfile(self.UBM_MODEL_FILE):
            try:
                from gmmset import GMMSetPyGMM

                if GMMSet is GMMSetPyGMM:
                    return GMMSet(ubm=GMM.load(self.UBM_MODEL_FILE))
            except Exception as e:
                print "Warning: failed to import gmmset. You may forget to compile gmm:"
                print e
                print "Try running `make -C src/gmm` to compile gmm module."
                print "But gmm from sklearn will work as well! Using it now!"
            return GMMSet()
        return GMMSet()

	# Запуск режиму тренування програми
    def train(self):
        self.gmmset = self._get_gmm_set()
        start = time.time()
        print "Start training..."
        for name, feats in self.features.iteritems():
            self.gmmset.fit_new(feats, name)
        print time.time() - start, " seconds"
		
	# Запуск режиму передбачення голоса диктора
    def predict(self, fs, signal):
        try:
            feat = mix_feature((fs, signal))
        except Exception as e:
            print tb.format_exc()
            return None
        return self.gmmset.predict_one(feat)

	# Для виведення у файл бази даних
    def dump(self, fname):
        self.gmmset.before_pickle()
        with open(fname, 'w') as f:
            pickle.dump(self, f, -1)
        self.gmmset.after_pickle()

	# Завантаження файлу бази даних
    @staticmethod
    def load(fname):
        with open(fname, 'r') as f:
            R = pickle.load(f)
            R.gmmset.after_pickle()
            return R