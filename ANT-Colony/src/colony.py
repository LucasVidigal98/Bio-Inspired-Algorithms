from ant import Ant
import math
import random


class Colony:
    def __init__(self, tsp, alpha, beta, r):
        self.tsp = tsp
        self.ants = list()
        self.pheromone = list()
        self.max = 10
        self.alpha = alpha
        self.beta = beta
        self.Q = 500
        self.r = r
        self.fo_star = 1000000
        self.path_star = list()

        for i in range(tsp.n):
            self.ants.append(Ant(i))
            self.ants[i].initialize(tsp.n)

        for i in range(tsp.n):
            column = list()
            for j in range(tsp.n):
                if i != j:
                    column.append(math.pow(10, -16))
                else:
                    column.append(None)
            self.pheromone.append(column)

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

    def prob_i_j(self, i, j, ant):
        prob = math.pow(self.pheromone[i][j], self.alpha) * \
            math.pow(1/self.tsp.get_distance(i, j), self.beta)

        total = 0
        for visited in range(len(ant.visited_nodes)):
            if ant.visited_nodes[visited] == False:
                if i == visited:
                    continue
                total += math.pow(self.pheromone[i][visited], self.alpha) * \
                    math.pow(self.tsp.get_distance(i, visited), self.beta)

        prob /= total
        return prob

    def generate_ant_path(self, ant):
        len_path = 1
        # print(self.ants[ant].initial_node)
        # input('ok>')
        self.ants[ant].initial_node = random.randint(0, self.tsp.n-1)
        self.ants[ant].path.append(self.ants[ant].initial_node)
        self.ants[ant].current_node = self.ants[ant].initial_node
        while len_path < self.tsp.n:
            prob_list = list()
            for i in range(self.tsp.n):
                prob_list.append(0)

            i = self.ants[ant].current_node
            for node in range(self.tsp.n):
                if i == node or self.ants[ant].visited_nodes[node] == True:
                    continue
                prob_list[node] = self.prob_i_j(i, node, self.ants[ant])

            max_prob = max(prob_list)
            next_node = prob_list.index(max_prob)
            self.ants[ant].visited_edge[self.ants[ant].current_node][next_node] = True
            self.ants[ant].path.append(next_node)
            self.ants[ant].visited_nodes[next_node] = True
            self.ants[ant].current_node = next_node
            len_path += 1

    def update_pheromone(self):
        for i in range(self.tsp.n):
            for j in range(self.tsp.n):
                if i == j:
                    continue

                pheromone = (1-self.r) * self.pheromone[i][j]

                total = 0
                for ant in self.ants:
                    if ant.visited_edge[i][j]:
                        total += self.Q / self.get_fo(ant.path)

                self.pheromone[i][j] = pheromone + total

    def init(self):

        statitics = dict()
        best = dict()

        for i in range(self.max):
            generation = list()
            for ant in range(len(self.ants)):
                self.generate_ant_path(ant)
                generation.append(self.get_fo(self.ants[ant].path))
                # print(self.ants[ant].path)

            for ant in range(len(self.ants)):
                l_k = self.get_fo(self.ants[ant].path)
                if l_k < self.fo_star:
                    self.fo_star = l_k
                    self.path_star = self.ants[ant].path.copy()
            '''
            print('-'*35)
            print(f'Iteração: {i}')
            print(f'Melhor solução {self.fo_star}')
            print(f'Best Tuor: {self.path_star}')
            print('-'*35)
            '''

            self.update_pheromone()
            statitics[str(i)] = generation
            best[str(i)] = min(generation)

            for ant in range(len(self.ants)):
                self.ants[ant].path = list()
                self.ants[ant].visited_edge = list()
                self.ants[ant].visited_nodes = list()
                self.ants[ant].initialize(self.tsp.n)

        return statitics, best
