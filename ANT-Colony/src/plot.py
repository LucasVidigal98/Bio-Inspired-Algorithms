from matplotlib import pyplot as plt
import numpy as np
import pickle as pk
from os import sep


def plot_best(history, alpha, beta, r, file):
    fit = list()
    generation = list()

    for h in history.keys():
        fit.append(history[h])
        generation.append(h)

    plt.plot(generation, fit)
    plt.title('Fit x Gerações -')
    plt.xlabel('Gerações')
    plt.ylabel('Melhor Fit')
    path = f'..{sep}Graphics{sep}{file}_best_{alpha}_{beta}_{r}.png'
    print('Imagem gerada em -> ' + path)
    # plt.show()
    plt.savefig(path)
    plt.close()


def plot_mean(statitics, alpha, beta, r, file):
    fit = list()
    generation = list()

    for s in statitics.keys():
        fit.append(np.median(statitics[s]))
        generation.append(s)

    plt.plot(generation, fit)
    plt.title('Fit x Gerações - Média')
    plt.xlabel('Gerações')
    plt.ylabel('Melhor Fit')
    path = f'..{sep}Graphics{sep}{file}_median_{alpha}_{beta}_{r}.png'
    print('Imagem gerada em -> ' + path)
    # plt.show()
    plt.savefig(path)
    plt.close()
