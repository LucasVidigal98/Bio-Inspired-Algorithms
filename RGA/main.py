from AG import AG
from graphic import plot, partial_statics, generate_table, save_history
import sys

npop = 0
ngen = 0
nelite = 1
pc = 0
pm = 0
dimension = 0
alpha = 0
beta = 0
has_elite = 0

partial_statics_dict = dict()
total_history = dict()

try:
    npop = int(sys.argv[1])
    ngen = int(sys.argv[2])
    dimension = int(sys.argv[3])
    pc = float(sys.argv[4])
    pm = float(sys.argv[5])
    alpha = float(sys.argv[6])
    beta = float(sys.argv[7])
    has_elite = int(sys.argv[8])
except:
    npop = 100
    ngen = 100
    nelite = 1
    pc = 0.6
    pm = 0.01
    dimension = 30
    alpha = 0.15
    beta = 0.05
    has_elite = 1
    print('Erro nos parâmetros - Set default')

for execution in range(10):

    print('-'*30)
    print('Inicializando Execução de número ' + str(execution))
    print('Npop: ' + str(npop))
    print('Ngen: ' + str(ngen))
    print('Pc: ' + str(pc))
    print('Pm: ' + str(pm))
    print('Dimensão: ' + str(dimension))
    print('Alpha: ' + str(alpha))
    print('Beta: ' + str(beta))
    print('Elite? ' + str(has_elite))
    print('-'*30)
    genetic_algorithm = AG(npop, ngen, nelite, has_elite,
                           dimension, pc, pm, alpha, beta)
    history, statics_dict = genetic_algorithm.init()
    total_history[str(execution)] = history
    #plot(history, dimension)
    partial_statics(statics_dict, partial_statics_dict, execution)

save_history(total_history, npop, ngen, pc, pm, has_elite)
generate_table(npop, ngen, pc, pm, has_elite, partial_statics_dict)
