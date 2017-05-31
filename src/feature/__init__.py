# !/usr/bin/env python2
# -*- coding: UTF-8 -*-
# __init__.py - для імпорту і запуску бібліотек MFCC, LPC


import sys

try:
    import BOB as MFCC
except Exception as e:
    print >> sys.stderr, e
    print >> sys.stderr, "Warning: failed to import Bob, will use a slower version of MFCC instead."
    import MFCC
import LPC
import numpy as np


# Функція взаємодії алгоритмів MFCC та LPC
def mix_feature(tup):
    mfcc = MFCC.extract(tup)
    lpc = LPC.extract(tup)
    if len(mfcc) == 0:
        print >> sys.stderr, "ERROR.. failed to extract mfcc feature:", len(tup[1])
    return np.concatenate((mfcc, lpc), axis=1)
