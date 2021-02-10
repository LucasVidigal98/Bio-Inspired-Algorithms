import random
import math
import numpy as np
import operator
from SortObject import SortObject


class AG:
    def __init__(self, npop, ngen, nelite, precision, dimension, pc, pm):
        self.npop = npop
        self.ngen = ngen
        self.nelite = nelite
        self.precision = precision
        self.dimension = dimension
        self.pc = pc
        self.pm = pm
        self.xmin = -2
        self.xmax = 2

        self.pop = list()
        self.inter_pop = list()
        self.elite = [0, 0, 0, 0, 0, 0]
        self.fit_elite = 0
        for i in range(npop):
            genes = list()
            for i in range(self.precision*self.dimension):
                genes.append(0)
            self.pop.append(genes)

    def create_initial_pop(self):
        for i in range(self.npop):
            for j in range(self.precision*self.dimension):
                self.pop[i][j] = 0 if (random.randint(1, 100) % 2 == 0) else 1

    def convert_to_intger(self, x):
        integer_number = 0
        integer_array = list()
        init = 0
        final = self.precision
        for d in range(self.dimension):
            result = 0
            for i in range(init, final):
                integer_number += math.pow(2, i) * x[i]
                result = self.xmin + ((self.xmax-self.xmin) /
                                      (math.pow(2, 6) - 1)) * integer_number
            integer_array.append(result)
            init += self.precision
            final += self.precision

        return integer_array

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
            fit.append(self.get_fo(self.convert_to_intger(pop[i])))

        return fit

    def get_parents(self, fit):
        parents = list()
        npop = 0

        while npop < self.npop:
            p1 = random.randint(0, self.npop-1)
            p2 = random.randint(0, self.npop-1)
            while p1 == p2:
                p1 = random.randint(0, self.npop-1)

            winner = 0
            if fit[p2] > fit[p1]:
                winner = p1
            else:
                winner = p2

            parents.append(winner)
            npop += 1

        return parents

    def get_wrost_fit(self):
        fit = self.evaluate_pop(self.inter_pop)

        max_fit = max(fit)
        p_max = fit.index(max_fit)

        return p_max, max_fit

    def get_best_fit(self, fit):
        min_fit = min(fit)

        return min_fit, fit.index(min_fit)

    def crossover(self, parents):
        npop = 0
        offspring = list()

        for p in range(0, len(parents), 2):
            first_child = list()
            second_child = list()

            point = random.randint(0, self.dimension*self.precision)
            for i in range(point):
                first_child.append(self.pop[parents[p]][i])
                second_child.append(self.pop[parents[p+1]][i])
            for i in range(point, self.precision*self.dimension):
                first_child.append(self.pop[parents[p+1]][i])
                second_child.append(self.pop[parents[p]][i])

            offspring.append(first_child)
            offspring.append(second_child)

        self.inter_pop = offspring

    def mutation(self):
        for i in self.inter_pop:
            m = random.uniform(0, 1)
            if m <= self.pm:
                for gene in i:
                    gene = 0 if gene == 1 else 1

    def next_generation(self, offspring):
        sorted_offspring = list()
        for o in offspring:
            sorted_offspring.append(SortObject(
                o, self.get_fo(self.convert_to_intger(o))))

        sorted_offspring.sort(key=operator.attrgetter('fit'), reverse=True)
        for s in sorted_offspring:
            print(s.fit)
        input('ok>')

    def get_elite(self, g, fit):
        best_fit, p_best = self.get_best_fit(fit)

        if g == 0:
            self.elite = self.pop[p_best]
            self.fit_elite = best_fit
        else:
            if best_fit < self.fit_elite:
                self.elite = self.pop[p_best]
                self.fit_elite = best_fit

        p_max, _ = self.get_wrost_fit()
        self.inter_pop[p_max] = self.elite

    def init(self):
        self.create_initial_pop()
        history = list()

        generation = 0
        while generation < self.ngen:
            fit = self.evaluate_pop(self.pop)
            parents = self.get_parents(fit)
            self.crossover(parents)
            self.mutation()
            # self.next_generation(offspring)
            self.get_elite(generation, fit)
            self.pop = self.inter_pop
            best_fit, _ = self.get_best_fit(fit)
            history.append((best_fit, generation))
            '''
            print('-' * 25)
            print('Geração = ' + str(generation))
            print('Elite = ' + str(self.fit_elite))
            print('Melhor sol da Geração = ' + str(best_fit))
            print('-' * 25)
            # input('OK>')
            '''
            generation += 1

        return history
