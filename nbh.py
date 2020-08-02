# -*- coding: utf-8 -*-
"""
A new file.
"""
import numpy as np


# =============================================================================
# swap
# =============================================================================
def _swap(sol, pair):
    # pair: left in, right out
    next_sol = list(sol)
    next_sol.append(pair[0])
    next_sol.remove(pair[1])
    next_sol = tuple(sorted(next_sol))
    return next_sol


def neighbor_swap(n_dim, sol):
    res = tuple(set(range(n_dim)) - set(sol))
    pairs = [(res[i], sol[j]) for i, j in np.ndindex(len(res), len(sol))]
    swap_sols = [_swap(sol, pair) for pair in pairs]
    return swap_sols


# =============================================================================
# without tabu
# =============================================================================
def neighbor_current2back(curr_sol):
    back_sols = []
    for i in curr_sol:
        back_sol = list(curr_sol)
        back_sol.remove(i)
        back_sol = tuple(sorted(back_sol))
        back_sols.append(back_sol)
        pass
    return back_sols


def neighbor_back2current(n_dim, back_sol):
    res = tuple(set(range(n_dim)) - set(back_sol))
    curr_sols = []
    for i in res:
        curr_sol = list(back_sol)
        curr_sol.append(i)
        curr_sol = tuple(sorted(curr_sol))
        curr_sols.append(curr_sol)
        pass
    return curr_sols


# =============================================================================
# with tabu
# =============================================================================
def tabu_neighbor_current2back(curr_sol, HTB):
    back_sols = []
    for i in curr_sol:
        back_sol = list(curr_sol)
        back_sol.remove(i)
        back_sol = tuple(sorted(back_sol))
        if hash(back_sol) not in HTB:
            back_sols.append(back_sol)
        else:
            HTB[hash(back_sol)] += 1
        pass
    return back_sols


def tabu_neighbor_back2current(n_dim, back_sol, HTC):
    res = tuple(set(range(n_dim)) - set(back_sol))
    curr_sols = []
    for i in res:
        curr_sol = list(back_sol)
        curr_sol.append(i)
        curr_sol = tuple(sorted(curr_sol))
        if hash(curr_sol) not in HTC:
            curr_sols.append(curr_sol)
        else:
            HTC[hash(curr_sol)] += 1
        pass
    return curr_sols
