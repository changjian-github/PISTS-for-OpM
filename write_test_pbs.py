# -*- coding: utf-8 -*-
"""
A new file.
"""
import json
import os
import subprocess
from itertools import product


def build_folders():
    folders = ['logs',
               'logs/output',
               'logs/error',
               'submits']
    for folder in folders:
        try:
            os.mkdir(folder)
        except:
            pass
        pass
    pass


# change parameters here
def combine_parameters(block, names, n_proc, setting):
    paras = []
    for name in names:
        para = '{},{},{}-{}-{},{}'.format(name, n_proc, *setting, block)
        paras.append(para)
        pass
    return paras


def load_names(genre):
    file = 'name-table.json'
    with open(file, 'r') as f:
        name_table = json.load(f)
    names = name_table[genre]
    return names


def string_arguments(paras, script):
    arguments = []
    for para in paras:
        argument = '--para {}'.format(para)
        arguments.append(argument)
        pass
    return arguments


def string_job_array(arguments, job, script):
    txt = ('#!/bin/sh\n'
           '#PBS -N {0}\n'
           '#PBS -l ncpus=1\n'
           '#PBS -l partition=su02\n'
           '#PBS -l walltime=120:00:00\n'
           '#PBS -o logs/output/{0}.o\n'
           '#PBS -e logs/error/{0}.e\n'
           '#PBS -t 0-{1}\n\n'
           'cd $PBS_O_WORKDIR\n\n').format(job, len(arguments)-1)
    txt += 'ARGS=(\n'
    for argument in arguments:
        txt += '    "{}"\n'.format(argument)
        pass
    txt += (')\n\n'
            'python %s ${ARGS[$PBS_ARRAYID]}\n') % script
    return txt


def write_shell(job, paras, script, shell):
    build_folders()
    arguments = string_arguments(paras, script)
    string = string_job_array(arguments, job, script)
    with open(shell, 'w') as f:
        f.write(string)
    pass


def func(block, n_proc, GL, ND, TD):
    method = 'final'
    names = load_names('all')
    setting = [GL, ND, TD]
    build_folders()
    job = '{}-blk{}'.format(method, block)
    paras = combine_parameters(block, names, n_proc, setting)
    shell = 'submits/submit-{}.pbs'.format(job)
    script = 'run_{}.py'.format(method)
    write_shell(job, paras, script, shell)
    resp = subprocess.run(['dos2unix', shell], capture_output=True, encoding='gbk')
    print(resp.stderr)
    return shell


def main():
    n_proc = 12
    GL = 2800
    NDs = [1]
    TDs = [10]
    shells = []
    for i, (ND, TD) in enumerate(product(NDs, TDs)):
        shell = func(i, n_proc, GL, ND, TD)
        shells.append('qsub ' + shell)
        pass
    string = '\n'.join(shells)
    with open('batch.sh', 'w') as f:
        f.write(string)
    resp = subprocess.run(['dos2unix', 'batch.sh'], capture_output=True, encoding='gbk')
    print(resp.stderr)
    pass


if __name__ == '__main__':
    main()
    pass