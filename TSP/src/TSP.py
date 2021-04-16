class TSP:
    def __init__(self, n, dist_tsp, solution):
        self.n = n
        self.dist_tsp = dist_tsp
        self.solution = solution

    def get_distance(self, i, j):
        return self.dist_tsp[i][j]
