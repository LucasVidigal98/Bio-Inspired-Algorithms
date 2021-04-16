from AG import genetic
from ag_statics import calculate_statics, save_statics
import sys

try:
    npop = int(sys.argv[1])
    ngen = int(sys.argv[2])
    pc = float(sys.argv[3])
    pm = float(sys.argv[4])
except:
    print(
        'Erro nos parâmetros python3 main.py [npop] [ngen] [Taxa de cruzamento] [Taxa de Mutação]')
    sys.exit(0)

ga = genetic(npop, ngen, pc, pm)

best_values = list()
median = list()
dsvp = list()
best_history = list()

for i in range(0, 1):
    history, statics_dict = ga.init()
    best_values.append(history[len(history)-1][0])
    best_statics = calculate_statics(statics_dict)
    median.append(best_statics[0])
    dsvp.append(best_statics[1])
    best_history.append(history)

best = min(best_values)
best_index = best_values.index(best)

save_statics(best, median[best_index], dsvp[best_index],
             best_history[best_index], npop, ngen, pc, pm)


print(f'Mehlor execução: {best_index}')
print(f'Melhor FO: {best}')
print(f'Melhor Média: {median[best_index]}')
print(f'Melhor dsvp: {dsvp[best_index]}')
