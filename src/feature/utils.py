#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# utils.py - допоміжний файл для проміжних розрахунків

import numpy

kwd_mark = object()


# Для кешування результатів, скорочує час виконання програми
def cached_func(function):
    cache = {}

    def wrapper(*args, **kwargs):
        key = args + (kwd_mark,) + tuple(sorted(kwargs.items()))
        if key in cache:
            return cache[key]
        else:
            result = function(*args, **kwargs)
            cache[key] = result
            return result

    return wrapper


# Для обчислення різниці між масивами математичних коефіцієнтів
def diff_feature(feat, nd=1):
    diff = feat[1:] - feat[:-1]
    feat = feat[1:]
    if nd == 1:
        return numpy.concatenate((feat, diff), axis=1)
    elif nd == 2:
        d2 = diff[1:] - diff[:-1]
        return numpy.concatenate((feat[1:], diff[1:], d2), axis=1)

