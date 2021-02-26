from matplotlib import pyplot as plt
import numpy as np
import pickle as pk
from os import sep


def plot(history, dimension):
    fit = list()
    generation = list()

    for h in history:
        fit.append(h[0])
        generation.append(h[1])

    plt.plot(generation, fit)
    plt.title('Fit x Gerações -' + ' Dimensão = ' + str(dimension))
    plt.xlabel('Gerações')
    plt.ylabel('Melhor Fit')
    path = 'Graphics' + sep + 'Dimensao=' + str(dimension)
    print('Imagem gerada em -> ' + path)
    plt.show()
    # plt.savefig(path)


def partial_statics(statics_dict, partial_statics_dict, execution):
    mean_generation = list()
    std_generation = list()
    best_values = list()
    for key in statics_dict.keys():
        if '_best' in key:
            best_values.append(float(statics_dict[key]))
        else:
            mean_generation.append(float(statics_dict[key]["Media"]))
            std_generation.append(float(statics_dict[key]["DSVP"]))

    statics = dict()

    statics["Media_Ger"] = np.median(mean_generation)
    statics["DSVP_Ger"] = np.median(std_generation)
    statics["Media_Best"] = np.median(best_values)
    statics["DSVP_Best"] = np.std(best_values)

    partial_statics_dict[str(execution)] = statics


def generate_table(npop, ngen, pc, pm, elite, partial_statics_dict):
    geral_mean = list()
    geral_dsvp = list()
    best_mean = list()
    best_dsvp = list()

    for key in partial_statics_dict.keys():
        geral_mean.append(partial_statics_dict[key]["Media_Ger"])
        geral_dsvp.append(partial_statics_dict[key]["DSVP_Ger"])
        best_mean.append(partial_statics_dict[key]["Media_Best"])
        best_dsvp.append(partial_statics_dict[key]["DSVP_Best"])

    file = open('Table' + sep + 'Table.tsv', 'a')
    line = str(pc) + '\t' + str(elite) + '\t' + str(pm) + '\t' + str(ngen) + '\t' + \
        str(npop) + '\t' + str(np.median(best_mean)) + \
        '\t' + str(np.median(best_dsvp)) + '\t' + \
        str(np.median(geral_mean)) + '\t' + str(np.median(geral_dsvp)) + '\n'

    file.write(line)
    file.close()


def save_history(history, npop, ngen, pc, pm, elite):
    file_name = 'History' + sep + \
        str(pc) + '_' + str(elite) + '_' + str(pm) + \
        '_' + str(npop) + '_' + str(ngen) + '.txt'
    file = open(file_name, 'wb')
    pk.dump(history, file)
    file.close()
