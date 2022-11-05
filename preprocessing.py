# -*- coding: utf-8 -*-
import numpy as np
import os
import pandas as pd
import re


def build_folders():
    folders = ['data']
    for folder in folders:
        try:
            os.mkdir(folder)
        except:
            pass
        pass
    pass


def load_files(folder):
    file_list, name_list = [], []
    for root, dirs, files in os.walk(folder):
        for file in files:
            str_list = file.split('.')
            if len(str_list) > 2: # wipe out README.txt
                file_list.append(root + '/' + file)
                name = '{}-{}.{}'.format(str_list[0], str_list[3], str_list[4])
                name_list.append(name)
            pass
        break # depth one
        pass
    return file_list, name_list


def make_data(file, name):
    with open(file, 'r') as f:
        lines = f.read().split('\n\n')
    # parse
    l3_list = re.split('[{}]', lines[3])
    array = [list(map(eval, l.split(',')))
                 for l in l3_list[1:] if len(l) > 2]
    matrix = np.array(array).transpose()
    columns = ['f{}'.format(i) for i in range(matrix.shape[1])]
    indices = ['c{}'.format(i) for i in range(matrix.shape[0])]
    df = pd.DataFrame(matrix, columns=columns, index=indices)
    # save
    df.to_csv('data/{}.csv'.format(name))
    pass


def main():
    folder = 'OpM_LIB_2016'
    # dataset
    build_folders()
    files, names = load_files(folder)
    for file, name in zip(files, names):
        print('processing "{}"...'.format(name))
        make_data(file, name)
        pass
    pass


if __name__ == '__main__':
    main()
    pass
