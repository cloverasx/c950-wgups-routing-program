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
        self.nodes[to_node][from_node] = distance  # because the graph is undirected

    def get_distance(self, from_node, to_node):
        from_node = from_node.lower()
        to_node = to_node.lower()
        return self.nodes.get(from_node, {}).get(to_node)
