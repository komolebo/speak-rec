#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

from ltsd import LTSD_VAD


class VAD(object):
    def __init__(self):
        self.initted = False
        self.ltsd = LTSD_VAD()

    def init_noise(self, fs, signal):
        self.initted = True
        self.ltsd.init_params_by_noise(fs, signal)

    def filter(self, fs, signal):
        if not self.initted:
            raise Exception("NoiseFilter Not Initialized")
        filtered, intervals = self.ltsd.filter(signal)
        return filtered, intervals


if __name__ == "__main__":
    from scipy.io import wavfile
    import sys

    fs, bg = wavfile.read(sys.argv[1])
    vad = VAD()
    vad.init_noise(fs, bg)

    fs, sig = wavfile.read(sys.argv[2])
    vaded, intervals = vad.filter(fs, sig)
    wavfile.write('vaded.wav', fs, vaded)

