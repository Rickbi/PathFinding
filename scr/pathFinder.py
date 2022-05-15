# Dijkstra’s shortest path algorithm
from cmath import inf
from pprint import pprint

class Node:
    def __init__(self, value) -> None:
        self.value = value
        self.nodes = []
        self.path_sum = inf
        self.pre = None
    
    def add_node(self, node, weight) -> None:
        toAdd = node, weight
        self.nodes.append(toAdd)
        self.nodes.sort(key=lambda n:n[1])
        
    def __repr__(self) -> str:
        return f'N{self.value}'


class Dijkstra:
    def __init__(self, table) -> None:
        self.update_graph(table)
        self.visited = set()

    def update_graph(self, table):
        ly = len(table)
        lx = len(table[0])
        m = [[Node((x,y)) for x in range(lx)] for y in range(ly)]
        for x in range(lx):
            for y in range(ly):
                if x+1 < lx and table[y][x+1] == 0:
                    m[y][x].add_node(m[y][x+1], 1)
                if x-1 >= 0 and table[y][x-1] == 0:
                    m[y][x].add_node(m[y][x-1], 1)
                if y+1 < ly and table[y+1][x] == 0:
                    m[y][x].add_node(m[y+1][x], 1)
                if y-1 >= 0 and table[y-1][x] == 0:
                    m[y][x].add_node(m[y-1][x], 1)
        self.table = table
        self.graph = m
    
    def step(self):
        re = []
        for v in self.visited:
            weight_0 = v.path_sum
            for node, weight in v.nodes:
                if node not in self.visited:
                    total_weight = weight_0 + weight
                    if total_weight < node.path_sum:
                        node.path_sum = total_weight
                        node.pre = v
                    re.append(node)
        if re:
            n_min = min(re, key=lambda n:n.path_sum)
            self.visited.add(n_min)
            return True
        return False
    
    def set_start(self, start):
        start_node = self.graph[ start[1] ][ start[0] ]
        start_node.path_sum = 0
        self.visited = {start_node}

    def get_path(self, end):
        end_node = self.graph[ end[1] ][ end[0] ]
        path = []
        nl = end_node
        while nl:
            path.append(nl.value)
            nl = nl.pre
        return path[::-1]

    def find_path(self, start, end, tol=1000):
        self.set_start(start)
        
        for i in range(tol):
            if not self.step():
                #print(i)
                break
        
        return self.get_path(end)

    def get_status_table(self):
        return [[i.path_sum for i in line] for line in self.graph]


def show_map(m, start, end, path):
    ly = len(m)
    lx = len(m[0])
    m_c = [[ ('O',' ')[ m[y][x] == 0 ] for x in range(lx)] for y in range(ly)]
    m_c[ start[1] ][ start[0] ] = 'S'
    m_c[ end[1] ][ end[0] ] = 'X'

    for p in path[1:-1]:
        x, y = p
        m_c[ y ][ x ] = '*'

    pprint(m_c)


if __name__ == '__main__':
    # Run a test of the Dijkstra’s algorithm

    m = [
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    ]

    pprint(m)

    start = (0,0)
    end = (9,0)

    path_finder = Dijkstra(m)
    pprint(path_finder.get_status_table())
    path = path_finder.find_path(start, end)
    pprint(path_finder.get_status_table())    
    show_map(m, start, end, path)
