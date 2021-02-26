import random
import math
import numpy as np
import operator
from SortObject import SortObject


class AG:
    def __init__(self, npop, ngen, nelite, has_elite, dimension, pc, pm, alpha, beta):
        self.npop = npop
        self.ngen = ngen
        self.nelite = nelite
        self.dimension = dimension
        self.pc = pc
        self.pm = pm
        self.xmin = -2
        self.xmax = 2
        self.alpha = alpha
        self.beta = beta

        self.pop = list()
        self.inter_pop = list()
        self.elite = list()
        self.has_elite = has_elite
        self.fit_elite = 0
        for i in range(npop):
            genes = list()
            for i in range(self.dimension):
                genes.append(0)
            self.pop.append(genes)
            self.inter_pop.append(genes)

    def create_initial_pop(self):
        for i in range(self.npop):
            for j in range(self.dimension):
                self.pop[i][j] = random.uniform(self.xmin, self.xmax)

    def get_fo(self, x):
        n = float(len(x))
        f_exp = -0.2 * math.sqrt(1/n * sum(np.power(x, 2)))

        t = 0
        for i in range(0, len(x)):
            t += np.cos(2 * math.pi * x[i])

        s_exp = 1.0/n * t
        f = -20 * math.exp(f_exp) - math.exp(s_exp) + 20 + math.exp(1)

        return f

    def evaluate_pop(self, pop):
        fit = list()
        for i in range(self.npop):
            fit.append(self.get_fo(pop[i]))

        return fit

    def roullet(self, fit):
        total = 0
        for f in fit:
            total += 1/f

        rou = list()
        for f in fit:
            rou.append((1/f)/total)

        first_parent = 0
        second_parent = 0

        for i in range(2):
            value = random.uniform(0, 1)
            rou_sum = 0
            nparent = 0
            for j in range(self.npop):
                if rou_sum >= value:
                    if i == 0:
                        first_parent = nparent
                    else:
                        second_parent = nparent
                        if second_parent == first_parent:
                            j = 0
                            value = random.uniform(0, 1)
                            rou_sum = 0
                            nparent = 0
                            continue
                    break
                rou_sum += rou[j]
                nparent += 1

        return first_parent, second_parent

    def get_parents(self, fit):
        parents = list()
        for i in range(0, self.npop, 2):
            first_parent, second_parent = self.roullet(fit)
            parents.append(first_parent)
            parents.append(second_parent)

        return parents

    def get_wrost_fit(self):
        fit = self.evaluate_pop(self.inter_pop)

        max_fit = max(fit)
        p_max = fit.index(max_fit)

        return p_max, max_fit

    def get_best_fit(self, fit):
        min_fit = min(fit)

        return min_fit, fit.index(min_fit)

    def check_u_value(self, u):
        if u < -2:
            return -2
        elif u > 2:
            return 2

        return u

    def crossover(self, parents, fit):
        children = 0
        first_child = list()
        second_child = list()
        for i in range(self.dimension):
            first_child.append(i)
            second_child.append(i)

        for i in range(0, len(parents), 2):
            X = self.pop[parents[i]]
            Y = self.pop[parents[i+1]]

            if (1/fit[parents[i]]) < (1/fit[parents[i+1]]):
                X = self.pop[parents[i+1]]
                Y = self.pop[parents[i]]

            if random.uniform(0, 1) <= self.pc:
                for j in range(self.dimension):
                    d = abs((X[j] - Y[j]))
                    if X[j] <= Y[j]:
                        u = random.uniform(X[j]-self.alpha*d, Y[j]+self.beta*d)
                        u = self.check_u_value(u)
                        first_child[j] = u
                        u = random.uniform(X[j]-self.alpha*d, Y[j]+self.beta*d)
                        u = self.check_u_value(u)
                        second_child[j] = u
                    else:
                        u = random.uniform(Y[j]-self.beta*d, X[j]+self.alpha*d)
                        u = self.check_u_value(u)
                        first_child[j] = u
                        u = random.uniform(Y[j]-self.beta*d, X[j]+self.alpha*d)
                        u = self.check_u_value(u)
                        second_child[j] = u
                self.inter_pop[children] = first_child
                self.inter_pop[children+1] = second_child
            else:
                self.inter_pop[children] = X
                self.inter_pop[children+1] = Y

            children += 2

    def mutation(self):
        for individual in self.inter_pop:
            value = random.uniform(0, 1)
            if value <= self.pm:
                pos = random.randint(0, len(individual)-1)
                individual[pos] = random.uniform(self.xmin, self.xmax)

    def get_elite(self, g, fit):
        best_fit, p_best = self.get_best_fit(fit)

        if g == 0:
            self.elite = self.pop[p_best]
            self.fit_elite = best_fit
        else:
            if best_fit < self.fit_elite:
                self.elite = self.pop[p_best]
                self.fit_elite = best_fit

        pos = random.randint(0, self.npop-1)
        self.pop[pos] = self.elite

    def get_parcial_statics(self, statics_dict, gen, fit):
        gen_statics = dict()
        gen_statics["Media"] = np.median(fit)
        gen_statics["DSVP"] = np.std(fit)
        statics_dict[str(gen)] = gen_statics

    def get_final_statics(self, statics_dict, history):
        for h in history:
            statics_dict[str(h[1]) + '_best'] = h[0]

    def init(self):
        self.create_initial_pop()
        history = list()
        statics_dict = dict()

        generation = 0
        while generation < self.ngen:
            fit = self.evaluate_pop(self.pop)
            parents = self.get_parents(fit)
            self.crossover(parents=parents, fit=fit)
            self.mutation()
            self.get_parcial_statics(statics_dict, generation, fit)
            self.pop = self.inter_pop
            fit = self.evaluate_pop(self.pop)
            if self.has_elite == 1:
                self.get_elite(generation, fit)
            fit = self.evaluate_pop(self.pop)
            best_fit, _ = self.get_best_fit(fit)
            history.append((best_fit, generation))
            '''
            print('-' * 25)
            print('Geração = ' + str(generation))
            print('Elite = ' + str(self.fit_elite))
            print('Melhor sol da Geração = ' + str(best_fit))
            print('-' * 25)
            #input('OK>')
            '''
            generation += 1

        self.get_final_statics(statics_dict, history)

        return history, statics_dict
