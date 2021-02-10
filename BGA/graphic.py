from matplotlib import pyplot as plt
from os import sep


def plot(history, precision, dimension):
    fit = list()
    generation = list()

    for h in history:
        fit.append(h[0])
        generation.append(h[1])

    plt.plot(generation, fit)
    plt.title('Fit x Gerações - Precisão = ' +
              str(precision) + ' Dimensão = ' + str(dimension))
    plt.xlabel('Gerações')
    plt.ylabel('Melhor Fit')
    plt.savefig('Graphics' + sep + 'Precisao=' +
                str(precision) + 'Dimensao=' + str(dimension))
