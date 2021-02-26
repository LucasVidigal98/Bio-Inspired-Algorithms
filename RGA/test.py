import os

pm = [0.01, 0.05, 0.1]
pc = [0.6, 0.8, 1]
npop = [50, 100]
ngen = [50, 100]
has_elite = [0, 1]
alpha = 0.15
beta = 0.05
dimension = 30

for n in range(len(npop)):
    for pc_value in pc:
        for pm_value in pm:
            for elite in has_elite:
                os.system('python3 main.py ' + str(npop[n]) + ' ' + str(ngen[n]) + ' 30 ' + str(
                    pc_value) + ' ' + str(pm_value) + ' 0.15 0.05 ' + str(elite))
