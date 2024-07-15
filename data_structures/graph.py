from utils.string_utils import StringUtils as su


class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, name):
        if name not in self.nodes:
            self.nodes[name] = {}

    def add_edge(self, from_node, to_node, distance):
        self.add_node(from_node)
        self.add_node(to_node)
        self.nodes[from_node][to_node] = distance
        self.nodes[to_node][from_node] = distance

    def get_distance(self, from_node, to_node):
        from_node = su.clean_string(from_node)
        to_node = su.clean_string(to_node)
        return self.nodes.get(from_node, {}).get(to_node)

    def get_nodes(self):
        return list(self.nodes.keys())

    def get_edges(self):
        edges = []
        for from_node in self.nodes:
            for to_node in self.nodes[from_node]:
                edges.append((from_node, to_node, self.nodes[from_node][to_node]))
        return edges
