#!/usr/bin/python2
# -*- coding: utf-8 -*-
# ltsd.py - файл містить функції для видалення шуму

import sys
from scipy.io import wavfile
import matplotlib

matplotlib.use("Qt4Agg")
import matplotlib.pyplot as plt
import numpy as np

from pyssp.vad.ltsd import LTSD


MAGIC_NUMBER = 0.04644


# Клас для очищення сигналу від шуму
class LTSD_VAD(object):
    ltsd = None
    order = 5

    fs = 0
    window_size = 0
    window = 0

    lambda0 = 0
    lambda1 = 0

    noise_signal = None

	# Для ініціалізації полей класу
    def init_params_by_noise(self, fs, noise_signal):
        noise_signal = self._mononize_signal(noise_signal)
        self.noise_signal = np.array(noise_signal)
        self._init_window(fs)
        ltsd = LTSD(self.window_size, self.window, self.order)
        res, ltsds = ltsd.compute_with_noise(noise_signal,
                                             noise_signal)
        max_ltsd = max(ltsds)
        self.lambda0 = max_ltsd * 1.1
        self.lambda1 = self.lambda0 * 2.0
        print 'max_ltsd =', max_ltsd
        print 'lambda0 =', self.lambda0
        print 'lambda1 =', self.lambda1

	# Фільтруємо за допомогою бібліотечної функцію compute_with_noise
    def filter(self, signal):
        signal = self._mononize_signal(signal)
        res, ltsds = self._get_ltsd().compute_with_noise(signal, self.noise_signal)
        voice_signals = []
        res = [(start * self.window_size / 2, (finish + 1) * self.window_size
                / 2) for start, finish in res]
        print res, len(ltsds) * self.window_size / 2
        for start, finish in res:
            voice_signals.append(signal[start:finish])
        try:
            return np.concatenate(voice_signals), res
        except:
            return np.array([]), []

	# Для кожного вікна застосовуємо функцію Хеммінга
    def _init_window(self, fs):
        self.fs = fs
        self.window_size = int(MAGIC_NUMBER * fs)
        self.window = np.hanning(self.window_size)

	# Запуск конструктора класу
    def _get_ltsd(self, fs=None):
        if fs is not None and fs != self.fs:
            self._init_window(fs)
        return LTSD(self.window_size, self.window, self.order,
                    lambda0=self.lambda0, lambda1=self.lambda1)

	# Працюємо лише із моно-сигналами 
    def _mononize_signal(self, signal):
        if signal.ndim > 1:
            signal = signal[:, 0]
        return signal