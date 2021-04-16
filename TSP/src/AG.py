import random
import numpy as np


class AG:
    def __init__(self, npop, ngen, nelite, has_elite, pc, pm, tsp):
        self.npop = npop
        self.ngen = ngen
        self.nelite = nelite
        self.pc = pc
        self.pm = pm
        self.tsp = tsp
        self.stagnation = 0
        self.high_mutation_interation = 0

        self.pop = list()
        self.inter_pop = list()
        self.elite = list()
        self.has_elite = has_elite
        self.fit_elite = 0
        print('aqui')
        for i in range(npop):
            genes = list()
            for i in range(self.tsp.n):
                genes.append(0)
            self.pop.append(genes)
            self.inter_pop.append(genes)

    def create_initial_pop(self):
        for i in range(self.npop):

            in_path = list()
            for k in range(self.tsp.n):
                in_path.append(False)

            j = 0
            while j < self.tsp.n:
                node = random.randint(0, self.tsp.n-1)
                if in_path[node] == True:
                    continue
                self.pop[i][j] = node
                in_path[node] = True
                j += 1

    def get_fo(self, path):
        total = 0
        for p in range(len(path)):
            if p != (len(path)-1):
                total += self.tsp.get_distance(path[p], path[p+1])
        try:
            total += self.tsp.get_distance(path[len(path)-1], path[0])
        except:
            return 0

        return total

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
        n_parents = 0
        while n_parents < self.npop:
            first_parent, second_parent = self.roullet(fit)
            parents.append(first_parent)
            parents.append(second_parent)
            n_parents += 2

        return parents

    def get_wrost_fit(self):
        fit = self.evaluate_pop(self.inter_pop)

        max_fit = max(fit)
        p_max = fit.index(max_fit)

        return p_max, max_fit

    def get_best_fit(self, fit):
        min_fit = min(fit)

        return min_fit, fit.index(min_fit)

    def cross(self, first_parent, second_parent):
        children = list()
        for i in range(self.tsp.n):
            children.append(-1)

        delta = 0
        first_slice = 0
        second_slice = 0
        while delta == 0:
            first_slice = random.randint(0, self.tsp.n-1)
            second_slice = random.randint(first_slice, self.tsp.n-1)
            delta = second_slice - first_slice

        children[first_slice:second_slice] = first_parent[first_slice:second_slice]
        order_parent = list()
        for gene in second_parent:
            if (gene in children) == False:
                order_parent.append(gene)

        order = 0
        for j in range(second_slice, self.tsp.n):
            children[j] = order_parent[order]
            order += 1

        for j in range(0, first_slice):
            children[j] = order_parent[order]
            order += 1

        return children

    def crossover(self, parents, fit):
        children = 0

        for i in range(0, len(parents), 2):
            first_parent = self.pop[parents[i]]
            second_parent = self.pop[parents[i+1]]

            first_children = self.cross(first_parent, second_parent)
            second_children = self.cross(second_parent, first_parent)

            if random.uniform(0, 1) <= self.pc:
                self.inter_pop[children] = first_children
                self.inter_pop[children+1] = second_children
            else:
                self.inter_pop[children] = first_parent
                self.inter_pop[children+1] = second_parent

            children += 2

    def mutation(self):
        for individual in self.inter_pop:
            value = random.uniform(0, 1)
            if self.high_mutation_interation == 0:
                if value <= self.pm:
                    i = -1
                    j = -1
                    while i == j:
                        i = random.randint(0, len(individual)-1)
                        j = random.randint(0, len(individual)-1)

                    aux = individual[i]
                    individual[i] = individual[j]
                    individual[j] = aux
            else:
                #print('Alta mutação!!!!!!!!!!!!!!!!!!!!!!!!!!')
                if value <= 0.2:
                    i = -1
                    j = -1
                    while i == j:
                        i = random.randint(0, len(individual)-1)
                        j = random.randint(0, len(individual)-1)

                    aux = individual[i]
                    individual[i] = individual[j]
                    individual[j] = aux
                    self.high_mutation_interation += 1

    def get_elite(self, g, fit):
        best_fit, p_best = self.get_best_fit(fit)

        if g == 0:
            self.elite = self.pop[p_best].copy()
            self.fit_elite = best_fit
        else:
            if best_fit < self.fit_elite:
                self.elite = self.pop[p_best].copy()
                self.fit_elite = best_fit
            else:
                self.stagnation += 1
                if self.stagnation == 500:
                    self.stagnation = 0
                    self.high_mutation_interation = 1

                if self.high_mutation_interation == 4:
                    self.high_mutation_interation = 0

        pos = random.randint(0, self.npop-1)
        self.pop[pos] = self.elite

    def get_parcial_statics(self, statics_dict, gen, fit):
        gen_statics = dict()
        gen_statics["Media"] = np.median(fit)
        gen_statics["DSVP"] = np.std(fit)
        statics_dict[str(gen)] = gen_statics

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
            # input('OK>')
            '''
            generation += 1

        return history, statics_dict
