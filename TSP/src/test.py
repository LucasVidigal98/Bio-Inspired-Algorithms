import os

pm = [0.01, 0.05]
pc = [0.6, 1]
npop = [50]
ngen = [2500, 15000]
file = ['lau15', 'wg59']
#has_elite = [0, 1]
#alpha = 0.15
#beta = 0.05
#dimension = 30

for f in file:
    for n in npop:
        for gen in ngen:
            for p1 in pc:
                for p2 in pm:
                    os.system(f'python3 main.py {f} {n} {gen} {p1} {p2}')
