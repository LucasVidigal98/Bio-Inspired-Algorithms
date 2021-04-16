from matplotlib import pyplot as plt
import numpy as np
import pickle as pk
from os import sep


def plot_best(history, npop, ngen, pc, pm, file):
    fit = list()
    generation = list()

    for h in history:
        fit.append(h[0])
        generation.append(h[1])

    plt.plot(generation, fit)
    plt.title('Fit x Gerações -')
    plt.xlabel('Gerações')
    plt.ylabel('Melhor Fit')
    path = f'..{sep}Graphics{sep}{file}_Best_{npop}_{ngen}_{pc}_{pm}.png'
    print('Imagem gerada em -> ' + path)
    # plt.show()
    plt.savefig(path)
    plt.close()


def plot_mean(statics_dict, npop, ngen, pc, pm, file):
    fit = list()
    generation = list()

    for key in statics_dict.keys():
        fit.append(statics_dict[key]['Media'])
        generation.append(int(key))

    plt.plot(generation, fit)
    plt.title('Fit(Médio) x Gerações')
    plt.xlabel('Gerações')
    plt.ylabel('Fit(Médio)')
    path = f'..{sep}Graphics{sep}{file}_Mean_{npop}_{ngen}_{pc}_{pm}.png'
    print('Imagem gerada em -> ' + path)
    # plt.show()
    plt.savefig(path)
    plt.close()


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
    #statics["Media_Best"] = np.median(best_values)
    #statics["DSVP_Best"] = np.std(best_values)

    partial_statics_dict[str(execution)] = statics


def generate_table(npop, ngen, pc, pm, elite, partial_statics_dict, file):

    file = open('..' + sep + 'Table' + sep + f'{file}_Table.tsv', 'a')
    line = str(pc) + '\t' + str(elite) + '\t' + str(pm) + '\t' + str(ngen) + '\t' + \
        str(npop) + '\t' + \
        str(partial_statics_dict['0']["Media_Ger"]) + '\t' + \
        str(partial_statics_dict['0']["DSVP_Ger"]) + '\n'

    file.write(line)
    file.close()
