from io_files import read_file_dist, read_file_solution
from graphics import *
from TSP import TSP
from AG import AG
import sys

try:
    file = str(sys.argv[1])
    npop = int(sys.argv[2])
    ngen = int(sys.argv[3])
    pc = float(sys.argv[4])
    pm = float(sys.argv[5])
except:
    print('Erro nos argumentos')
    print('python3 main.py file_name(lau15 ou wg59) npop, ngen, pcruzamento, pmutação')
    sys.exit(1)

partial_statics_dict = dict()

n, dist_tsp = read_file_dist(file)
sol = read_file_solution(file)
tsp = TSP(n, dist_tsp, sol)
genetic = AG(npop, ngen, 1, 1, pc, pm, tsp)
history, statics_dict = genetic.init()
fo_star = genetic.get_fo(tsp.solution)
#print(f'Melhor Solução: {fo_star}')
plot_best(history, npop, ngen, pc, pm, file)
plot_mean(statics_dict, npop, ngen, pc, pm, file)
partial_statics(statics_dict, partial_statics_dict, 0)
generate_table(npop, ngen, pc, pm, 1, partial_statics_dict, file)
