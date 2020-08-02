# -*- coding: utf-8 -*-
"""
method in lab.
"""
import argparse
import json
import multiprocessing as mp
import numpy as np
import os
# local
from node import ISTS


def build_folders(block, setting):
    subfolder = 'final-blk{}'.format(block)
    paraconfig = 'GL{}-ND{}-TD{}'.format(*setting)
    folders = ['results',
               'results/{}'.format(subfolder),
               'results/{}/{}'.format(subfolder, paraconfig)]
    for folder in folders:
        try:
            os.mkdir(folder)
        except:
            pass
        pass
    pass


def worker(name, setting, HTB, HTC):
    ists = ISTS(setting)
    ists.initialize(name)
    ists.start(HTB, HTC)
    outputs = ists.outputs
    step = ists.local_step
    dura = ists.dura
    return outputs, step, dura


def run(name, n_proc, setting):
    # process
    HTB = mp.Manager().dict()
    HTC = mp.Manager().dict()
    pool = mp.Pool(processes=n_proc)
    resps = []
    for i in range(n_proc):
        resp = pool.apply_async(worker, [name, setting, HTB, HTC])
        resps.append(resp)
        pass
    pool.close()
    pool.join()
    # get
    best_sols, best_objs, hit_times, steps, duras = [], [], [], [], []
    for resp in resps:
        outputs, step, dura = resp.get()
        best_sol, best_obj, hit_time = outputs
        best_sols.append(best_sol)
        best_objs.append(best_obj)
        hit_times.append(hit_time)
        steps.append(step)
        duras.append(dura)
        pass
    best_objs = np.array(best_objs)
    hit_times = np.array(hit_times)
    hit_indices = np.max(best_objs)==best_objs
    opt_idx = hit_times.tolist().index(np.min(hit_times[hit_indices]))
    SUM = {}
    SUM['best_sol'] = str(best_sols[opt_idx])
    SUM['best_obj'] = best_objs[opt_idx]
    SUM['hit_time'] = round(hit_times[opt_idx], 2)
    SUM['num_step'] = steps[opt_idx]
    SUM['duration'] = round(duras[opt_idx], 2)
    return SUM, dict(HTB), dict(HTC)


def parse_parameters(para):
    # para = "name,n_proc,setting,block"
    str_list = para.split(',')
    name = str_list[0]
    n_proc = eval(str_list[1])
    setting = list(map(eval, str_list[2].split('-')))
    block = eval(str_list[3])
    return name, n_proc, setting, block


def main(args):
    name, n_proc, setting, block = parse_parameters(args.para)
    SUM, HTB, HTC = run(name, n_proc, setting)
    build_folders(block, setting)
    subfolder = 'final-blk{}'.format(block)
    paraconfig = 'GL{}-ND{}-TD{}'.format(*setting)
#    genres = ['SUM', 'HTB', 'HTC'] # uncomment to save tabu list
#    tables = [SUM, HTB, HTC] # uncomment to save tabu list
    genres = ['SUM']
    tables = [SUM]
    for genre, table in zip(genres, tables):
        json_file = 'results/{}/{}/{}-{}.json'.format(
            subfolder, paraconfig, name, genre)
        with open(json_file, 'w') as f:
            json.dump(table, f, indent=4)
        pass
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--para', type=str)
    args = parser.parse_args()
    main(args)
    pass
