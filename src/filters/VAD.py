#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# VAD.py - для фільтрації шумів у сигналі

from ltsd import LTSD_VAD


# Клас для фільтрації шумів
class VAD(object):
    def __init__(self):
        self.initted = False
        self.ltsd = LTSD_VAD()

    # Пошук шумів
	def init_noise(self, fs, signal):
        self.initted = True
        self.ltsd.init_params_by_noise(fs, signal)

	# Фільтрація шумів
    def filter(self, fs, signal):
        if not self.initted:
            raise Exception("NoiseFilter Not Initialized")
        filtered, intervals = self.ltsd.filter(signal)
        return filtered, intervals

