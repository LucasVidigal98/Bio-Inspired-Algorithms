import os

pop = [25, 50, 100]
ngen = [100, 50, 25]
pc = [0.4, 0.6, 0.8]
pm = [0.1, 0.2, 0.4]

for i in range(len(pop)):
    for c in pc:
        for m in pm:
            print(f'Iniciando execuçao -> {pop[i]} {ngen[i]} {c} {m}')
            print(f'python3 main.py {pop[i]} {ngen[i]} {c} {m}')
            print(f'Finalizando execuçao -> {pop[i]} {ngen[i]} {c} {m}')
