# -*- coding: utf-8 -*-
"""
A new file.
"""
import numpy as np
import pandas as pd
import re
import time


# =============================================================================
# tool function
# =============================================================================
def timeit(func):
    def wrapper(*args, **kw):
        t = time.perf_counter()
        r = func(*args, **kw)
        print("time consumed: {:.2e}".format(time.perf_counter()-t))
        return r
    return wrapper


# =============================================================================
# util function
# =============================================================================
def extract_dataset(name):
    file = 'data/{}.csv'.format(name)
    data = pd.read_csv(file, index_col=0).values
    level = eval(re.split(r'[.-]', name)[1][1:])
    return data, level


def objective(data, sol):
    obj = sum(np.min(data[:, sol], axis=1))
    return obj