import math
from particule import Particule
import numpy as np
from random import uniform


class PSO:
    def __init__(self, w, c1, c2, m, max_iter):
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.m = m
        self.max_iter = max_iter
        self.pop = list()
        self.g_best = list()
        self.best = 100000000

        for i in range(m):
            particule = Particule(-10, 10, 4, self)
            particule.init_particule()
            self.pop.append(particule)

        for p in self.pop:
            if p.best < self.best:
                self.best = p.best
                self.g_best = p.p_best.copy()

    def get_fo(self, x):
        fo = 100*math.pow((x[0]-math.pow(x[1], 2)), 2) + math.pow((1-x[0]), 2) + 90*math.pow((x[3]-math.pow(x[2], 2)), 2) + \
            math.pow((1-x[2]), 2) + 10.1*(math.pow((x[1]-1), 2) +
                                          math.pow((x[3]-1), 2)) + 19.8*(x[1]-1)*(x[3]-1)

        return fo

    def init(self):

        history = list()

        for i in range(self.max_iter):
            for p in self.pop:
                fo_x = self.get_fo(p.x)
                if fo_x < p.best:
                    p.best = fo_x
                    p.p_best = p.x.copy()

                    if fo_x < self.best:
                        self.best = fo_x
                        self.g_best = p.x.copy()

                # Calculcar velocidade
                for j in range(4):
                    r1 = uniform(0, 1)
                    r2 = uniform(0, 1)
                    p.v[j] = self.w*p.v[j] + self.c1*r1 * \
                        (p.p_best[j]-p.x[j]) + self.c2 * \
                        r2*(self.g_best[j]-p.x[j])

                p.x = np.array(p.x) + np.array(p.v)

            history.append((i, round(self.best, 2)))

            print('-'*35)
            print(f'Iteração {i}')
            print(f'Posição da melhor Partícula {self.g_best}')
            print(f'Valor da FO {self.best}')
            print('-'*35)

        return history, self.g_best
