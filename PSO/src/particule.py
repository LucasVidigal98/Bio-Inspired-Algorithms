from random import randint
#from PSOA import PSO


class Particule():
    def __init__(self, xmin, xmax, n, PSO):
        self.x = list()
        self.v = list()
        self.p_best = list()
        self.best = 1000000
        self.xmin = xmin
        self.xmax = xmax
        self.n = n
        self.PSO = PSO

    def init_particule(self):
        for i in range(self.n):
            self.x.append(randint(-10, 10))
            self.p_best.append(self.x[i])
            self.v.append(0)

        self.best = self.PSO.get_fo(self.x)
