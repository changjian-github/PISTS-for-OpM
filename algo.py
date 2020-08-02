# -*- coding: utf-8 -*-
"""
A new file.
"""
import numpy as np
import time
from random import sample
# local
from nbh import (
    tabu_neighbor_back2current,
    tabu_neighbor_current2back
)
from util import objective


# =============================================================================
# tabu search
# =============================================================================
def tabu_search(self, curr_sol, curr_obj, HTB, HTC):
    best_sol, best_obj = curr_sol, curr_obj
    count = 0
    while True:
        # global exit condition
        if self.local_step >= 20 * self.level:
            self._exit = True
            break
        # update local step
        self.local_step += 1
        # delete-add local search
        back_sol, back_obj = _map_c2b_wt(self, curr_sol, HTB)
        if not back_obj:
            break
        curr_sol, curr_obj = _map_b2c_wt(self, back_sol, HTC)
        if not curr_obj:
            break
        # update tabu optimum
        if curr_obj > best_obj:
            best_sol = curr_sol
            best_obj = curr_obj
            count = 0
        else:
            count += 1
        # condition: search depth surpassed
        if count >= self.tabu_depth:
            break
        pass
    # update tabu_step
    self.tabu_step += 1
    return best_sol, best_obj


def _map_c2b_wt(self, curr_sol, HTB):
    c2b_sols = tabu_neighbor_current2back(curr_sol, HTB)
    if c2b_sols:
        c2b_objs = np.array(
            [objective(self.data, c2b_sol) for c2b_sol in c2b_sols]
        )
        c2b_midx = np.argmax(c2b_objs)
        back_sol = c2b_sols[c2b_midx]
        back_obj = c2b_objs[c2b_midx]
        HTB[hash(back_sol)] = 1
    else:
        back_sol = (0, ) * (self.level - 1)
        back_obj = 0
    return back_sol, back_obj


def _map_b2c_wt(self, back_sol, HTC):
    b2c_sols = tabu_neighbor_back2current(self.dim, back_sol, HTC)
    if b2c_sols:
        b2c_objs = np.array(
            [objective(self.data, b2c_sol) for b2c_sol in b2c_sols]
        )
        b2c_midx = np.argmax(b2c_objs)
        curr_sol = b2c_sols[b2c_midx]
        curr_obj = b2c_objs[b2c_midx]
        HTC[hash(curr_sol)] = 1
    else:
        curr_sol = (0, ) * self.level
        curr_obj = 0
    return curr_sol, curr_obj


# =============================================================================
# neighbor search
# =============================================================================
def specific_neighbor_search(self, best_sol, best_obj, HTB, HTC):
    count = 0
    while True:
        if self._exit:
            break
        # perturbation
        res = set(range(self.dim)) - set(best_sol)
        min_l = min(self.level, self.dim - self.level)
        # condition: distance too far
        if self._step_num > min_l:
            self._move_flag = True
            break
        else:
            temp_sol = _perturb(self, res, best_sol)
            temp_obj = objective(self.data, temp_sol)
        # tabu search
        stag_sol, stag_obj = tabu_search(self, temp_sol, temp_obj, HTB, HTC)
        # condition: better solution found
        if stag_obj > best_obj:
            best_sol = stag_sol
            best_obj = stag_obj
            self._move_flag = True
            count = 0
            break
        else:
            count += 1
        # condition: reach range
        if count >= self.neighbor_depth:
            self._move_flag = False
            break
        pass
    return best_sol, best_obj


def _perturb(self, res, sol):
    outers = sample(set(sol), self._step_num)
    inners = sample(set(res), self._step_num)
    new_sol = set(list(sol) + inners) - set(outers)
    new_sol = tuple(sorted(new_sol))
    return new_sol


# =============================================================================
# global search
# =============================================================================
def variable_global_search(self, init_sol, init_obj, HTB, HTC):
    # info
    paraconfig = 'GL: {}, ND: {}, TD: {}'.format(
        self.global_limit, self.neighbor_depth, self.tabu_depth)
    print(paraconfig)
    # head
    best_sols, best_objs, durations = [], [], []
    t0 = time.time()
    best_sol, best_obj = tabu_search(self, init_sol, init_obj, HTB, HTC)
    duration = time.time() - t0
    self.dura = duration
    best_sols.append(best_sol)
    best_objs.append(best_obj)
    durations.append(duration)
    self._step_num = 2 # solution is 1-NN optimal, step_num should be 2 at least.
    # body
    while True:
        print('scanning at {}-NN...'.format(self._step_num))
        best_sol, best_obj = specific_neighbor_search(
            self, best_sol, best_obj, HTB, HTC)
        duration = time.time() - t0
        self.dura = duration
        best_sols.append(best_sol)
        best_objs.append(best_obj)
        durations.append(duration)
        # better solution found
        if self._move_flag:
            self._step_num = 2 # step_num restart
        else:
            self._step_num += 1
        # condition: time up or step up
        if duration >= self.global_limit or self._exit:
            max_idx = np.argmax(best_objs)
            best_sol = best_sols[max_idx]
            best_obj = best_objs[max_idx]
            duration = durations[max_idx]
            break
        pass
    return best_sol, best_obj, duration
