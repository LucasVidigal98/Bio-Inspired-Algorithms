from matplotlib import pyplot as plt
from os import sep


def plot(history, w, c1, c2):
    fit = list()
    generation = list()

    for h in history:
        fit.append(h[1])
        generation.append(h[0])

    plt.plot(generation, fit)
    plt.title(f'Fit x Gerações - W = {w} C1 = {c1} C2 = {c2}')
    plt.xlabel('Gerações')
    plt.ylabel('Melhor Fit')
    path = f'Graphics{sep}W{w}_C1{c1}_C2_{c2}.png'
    print('Imagem gerada em -> ' + path)
    plt.savefig(path)
