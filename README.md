# Project description
 This is source code for paper <a href="https://www.sciencedirect.com/science/article/abs/pii/S0305054820302720/">Parallel iterative solution-based tabu search for the obnoxious p-median problem</a>

# Original dataset(deprecated)
1. download original dataset and result from this <a href="http://grafo.etsii.urjc.es/optsicom/opm/">site</a>.
2. unzip dataset to project directory "PISTS-for-OpM-master".
3. run "python preprocess.py" to transform ".txt" files to ".csv" files

# How to use
1. "run.bat" is to test a single instance on a local machine (Windows only).
2. "write_test_pbs.py" is to write job submission to a PBS cluster.
3. "result-info.json" stores the solutions and objectives obtained from this method.
