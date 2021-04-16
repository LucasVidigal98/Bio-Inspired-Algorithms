from io_files import read_file_dist, read_file_solution
from TSP import TSP
from colony import Colony
from plot import plot_best, plot_mean
import sys
import numpy as np
from os import sep


def calculate_statitics(partial_statics_dict, statitics):
    for s in statitics.keys():
        median = (np.median(statitics[s]))
        std = (np.std(statitics[s]))
        aux = dict()
        aux['median'] = median
        aux['std'] = std
        partial_statics_dict[s] = aux


def generate_table(partial_statics, alpha, beta, r, file):
    file = open(f'..{sep}Table/{file}.tsv', 'a')
    median = list()
    std = list()

    for s in partial_statics_dict.keys():
        median.append(float(partial_statics_dict[s]['median']))
        std.append(float(partial_statics_dict[s]['std']))

    line = str(alpha) + '\t' + str(beta) + '\t' + str(r) + '\t' + \
        str(np.median(median)) + '\t' + str(np.std(std)) + '\n'
    file.write(line)


try:
    file = str(sys.argv[1])
    alpha = int(sys.argv[2])
    beta = int(sys.argv[3])
    r = float(sys.argv[4])
except:
    print('Erro nos argumentos')
    sys.exit(1)

partial_statics_dict = dict()

n, dist_tsp = read_file_dist(file)
sol = read_file_solution(file)
tsp = TSP(n, dist_tsp, sol)
col = Colony(tsp, alpha, beta, r)
statitics, best = col.init()
calculate_statitics(partial_statics_dict, statitics)
generate_table(partial_statics_dict, alpha, beta, r, file)
# print(statitics)
# print(partial_statics_dict)
plot_best(best, alpha, beta, r, file)
#plot_mean(statitics, alpha, beta, r, file)
