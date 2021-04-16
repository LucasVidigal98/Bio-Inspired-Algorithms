#!/usr/bin/python3

import itertools
import os

instances = ['wg59']
iterations = [15]
alpha = [1, 5, 10]
beta = [1, 5, 10]
q = [500]
rho = [0.25, 0.5, 0.75]

all_list = [instances, iterations, alpha, beta, q, rho]
parameters = list(itertools.product(*all_list))
print(len(parameters))

for index, parameter in enumerate(parameters):
    print("Teste: " + str(parameter[0]) + " " + str(
        parameter[2]) + " " + str(parameter[3]) + " " + str(parameter[5]))
    os.system("python3 main.py " + str(parameter[0]) + " " + str(
        parameter[2]) + " " + str(parameter[3]) + " " + str(parameter[5]))
