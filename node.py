# -*- coding: utf-8 -*-
"""
A new file.
"""
from random import sample
# local
from algo import variable_global_search
from util import extract_dataset, objective


class ISTS:
    def __init__(self, setting):
        self.global_limit = setting[0]
        self.neighbor_depth = setting[1]
        self.tabu_depth = setting[2]
    def initialize(self, name):
        self.data, self.level = extract_dataset(name)
        self.name = name
        self.dim = self.data.shape[1]
        self.local_step = 0
        self.tabu_step = 0
        # support
        self._exit = False
    def start(self, HTB, HTC):
        init_sol = tuple(sorted(sample(range(self.dim), self.level)))
        init_obj = objective(self.data, init_sol)
        self.outputs = variable_global_search(self, init_sol, init_obj, HTB, HTC)
    pass
