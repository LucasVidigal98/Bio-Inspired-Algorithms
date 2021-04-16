from PDRC import pdcr
from random import randint, uniform
import math
import numpy as np


class genetic:
    def __init__(self, npop=int(), max_iter=int(), pc=int(), pm=int()):
        self.npop = npop
        delta = self.npop % 2
        self.max_iter = max_iter
        self.pop = list()
        self.inter_pop = list()
        self.diet_problem = pdcr()
        self.pc = pc
        self.pm = pm
        self.elite = dict()
        self.fit_elite = 100000

        if delta != 0:
            self.npop += 1

        for i in range(self.npop):
            aux_list = list()
            for j in range(self.diet_problem.mp.diet_scope["length"]):
                aux_list.append(j)

            self.pop.append({"proportion": aux_list, "id": aux_list})
            self.inter_pop.append({"proportion": aux_list, "id": aux_list})

    def init_pop(self):
        for individual in self.pop:
            aux = list()
            for i in range(self.diet_problem.mp.diet_scope["length"]):
                aux.append(
                    round(uniform(self.diet_problem.pi[0], self.diet_problem.pi[1]), 2))

            individual["proportion"] = aux.copy()

            aux = list()

            for i in range(self.diet_problem.mp.diet_scope["length"]):
                food = self.diet_problem.mp.diet_scope["composition"][i]
                interval = self.diet_problem.mp.food_interval[food]
                aux.append(randint(interval[0], interval[1]))

            individual['id'] = aux.copy()

    def evaluate_pop(self):
        fit = list()
        for individual in self.pop:
            fo = self.diet_problem.get_fo(
                individual["proportion"], individual["id"])
            fit.append(fo)

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
            value = uniform(0, 1)
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
                            value = uniform(0, 1)
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

    def mutation(self, meal, children=dict()):
        if uniform(0, 1) <= self.pm:
            init = self.diet_problem.mp.diet_scope[meal][0]
            final = self.diet_problem.mp.diet_scope[meal][1]
            for i in range(init, final+1):
                normal = np.random.normal(children["proportion"][i], 0.2)

                if normal < self.diet_problem.pi[0]:
                    normal = self.diet_problem.pi[0]
                if normal > self.diet_problem.pi[1]:
                    normal = self.diet_problem.pi[1]

                children["proportion"][i] = normal

                food = self.diet_problem.mp.diet_scope["composition"][i]
                interval = self.diet_problem.mp.food_interval[food]
                new_id = randint(interval[0], interval[1])

                children["id"][i] = new_id

    def cross(self, first_parent=dict(), second_parent=dict()):
        children = dict()
        aux_list = list()
        for j in range(self.diet_problem.mp.diet_scope["length"]):
            aux_list.append(j)

        children["proportion"] = aux_list
        children["id"] = aux_list
        children["proportion"] = first_parent["proportion"].copy()
        children["id"] = first_parent["id"].copy()

        meal_index = randint(0, self.diet_problem.mp.diet_scope["n_meals"]-1)
        meal = self.diet_problem.mp.diet_scope["meals"][meal_index]

        init = self.diet_problem.mp.diet_scope[meal][0]
        final = self.diet_problem.mp.diet_scope[meal][1]
        for i in range(init, final+1):
            children["proportion"][i] = second_parent["proportion"][i]
            children["id"][i] = second_parent["id"][i]

        self.mutation(meal, children)

        return children

    def crossover(self, parents=list(), fit=list()):
        children = 0

        for i in range(0, len(parents), 2):
            first_parent = self.pop[parents[i]]
            second_parent = self.pop[parents[i+1]]

            first_children = self.cross(first_parent, second_parent)
            second_children = self.cross(second_parent, first_parent)

            if uniform(0, 1) <= self.pc:
                self.inter_pop[children] = first_children.copy()
                self.inter_pop[children+1] = second_children.copy()
            else:
                self.inter_pop[children] = first_parent.copy()
                self.inter_pop[children+1] = second_parent.copy()

            children += 2

    def get_best_fit(self, fit):
        min_fit = min(fit)

        return min_fit, fit.index(min_fit)

    def get_elite(self, g, fit):
        best_fit, p_best = self.get_best_fit(fit)

        if g == 0:
            self.elite = self.pop[p_best].copy()
            self.fit_elite = best_fit
        else:
            if best_fit < self.fit_elite:
                self.elite = self.pop[p_best].copy()
                self.fit_elite = best_fit

        pos = randint(0, self.npop-1)
        self.pop[pos] = self.elite

    def get_parcial_statics(self, statics_dict, gen, fit):
        gen_statics = dict()
        gen_statics["Media"] = np.median(fit)
        gen_statics["DSVP"] = np.std(fit)
        statics_dict[str(gen)] = gen_statics

    def init(self):
        self.init_pop()
        history = list()
        statics_dict = dict()

        generation = 1
        while generation <= self.max_iter:
            fit = self.evaluate_pop()
            parents = self.get_parents(fit)
            self.crossover(parents, fit)
            self.get_parcial_statics(statics_dict, generation, fit)
            self.pop = self.inter_pop
            fit = self.evaluate_pop()
            self.get_elite(generation, fit)
            fit = self.evaluate_pop()
            best_fit, _ = self.get_best_fit(fit)
            history.append((best_fit, generation))

            print('-' * 25)
            print('Geração = ' + str(generation))
            print('Elite = ' + str(self.fit_elite))
            print('Melhor sol da Geração = ' + str(best_fit))
            print('-' * 25)
            # input('OK>')

            generation += 1

        print('SOL FINAL')
        self.diet_problem.get_fo(self.elite["proportion"], self.elite["id"])

        return history, statics_dict
