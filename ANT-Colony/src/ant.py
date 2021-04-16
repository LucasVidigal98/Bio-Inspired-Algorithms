class Ant:
    def __init__(self, id_ant):
        self.id = id_ant
        self.initial_node = id_ant
        self.current_node = self.initial_node
        self.path = list()
        self.visited_edge = list()
        self.visited_nodes = list()

    def initialize(self, n):
        for i in range(n):
            column_visited = list()
            column_prob = list()
            for j in range(n):
                if i != j:
                    column_visited.append(False)
                else:
                    column_visited.append(None)
            self.visited_edge.append(column_visited)

        for i in range(n):
            self.visited_nodes.append(False)
