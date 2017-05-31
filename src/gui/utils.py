#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# utils.py - Файл із допоміжними функціями введення-виведення

from scipy.io import wavfile


# Для зчитування сигнала
def read_wav(fname):
    fs, signal = wavfile.read(fname)
    if len(signal.shape) == 1:
        return fs, signal
    elif len(signal.shape) == 2:
        mono = [x[0] for x in signal]
        return fs, mono
    assert 1 == 2, "Wild error"


# Для запису сигнала
def write_wav(fname, fs, signal):
    wavfile.write(fname, fs, signal)

# Для виведення часу
def time_str(seconds):
    minutes = int(seconds / 60)
    sec = int(seconds % 60)
    return "{:02d}:{:02d}".format(minutes, sec)


# Стерео у моно
def monophonic(signal):
    if signal.ndim > 1:
        signal = signal[:, 0]
    return signal
