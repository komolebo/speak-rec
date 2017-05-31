#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# Файл з LPC методом

from math import isnan

import time
from scikits.talkbox.linpred import levinson_lpc
from numpy import *
from scipy.io import wavfile
from MFCC import hamming
from utils import cached_func, diff_feature


# Клас для роботи і керування LPC-параметрами
class LPCExtractor(object):
    def __init__(self, fs, win_length_ms, win_shift_ms, n_lpc,
                 pre_emphasis_coef):
        self.PRE_EMPH = pre_emphasis_coef
        self.n_lpc = n_lpc

        self.FRAME_LEN = int(float(win_length_ms) / 1000 * fs)
        self.FRAME_SHIFT = int(float(win_shift_ms) / 1000 * fs)
        self.window = hamming(self.FRAME_LEN)
	
	
	# Виклик алгоритму Левінсона знаходження коефіцієнтів
    def lpcc(self, signal):
        lpc = levinson_lpc.lpc(signal, self.n_lpc)[0]
        return lpc[1:]

		
	# Ділимо сигнал на фрагменти, для кожного фрагменту запускаємо lpc-алгоритм
    def extract(self, signal):
        frames = (len(signal) - self.FRAME_LEN) / self.FRAME_SHIFT + 1
        feature = []
        for f in xrange(frames):
            frame = signal[f * self.FRAME_SHIFT: f * self.FRAME_SHIFT +
                                                 self.FRAME_LEN] * self.window
            frame[1:] -= frame[:-1] * self.PRE_EMPH
            feature.append(self.lpcc(frame))

        feature = array(feature)
        feature[isnan(feature)] = 0
        return feature


# Запуск алгоритму LPC
@cached_func
def get_lpc_extractor(fs, win_length_ms=32, win_shift_ms=16,
                      n_lpc=15, pre_emphasis_coef=0.95):
    ret = LPCExtractor(fs, win_length_ms, win_shift_ms, n_lpc, pre_emphasis_coef)
    return ret

	
# Для перевірки сигналу і запуску get_lpc_extractor
def extract(fs, signal=None, diff=False, **kwargs):
    """accept two argument, or one as a tuple"""
    if signal is None:
        assert type(fs) == tuple
        fs, signal = fs[0], fs[1]
    signal = cast['float'](signal)
    ret = get_lpc_extractor(fs, **kwargs).extract(signal)
    if diff:
        return diff_feature(ret)
    return ret
