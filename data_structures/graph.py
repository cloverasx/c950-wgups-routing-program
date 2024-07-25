from utils.string_utils import StringUtils as su


class Graph:
    def __init__(self, file_path=None):
        self.nodes = {}
        if file_path:
            self.load_distance_graph(file_path)

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

    # This class doubles the necessary data and should be optimized to only have one
    # instance of each node-edge-node relationship since they're symmetric. This isn't
    # a critical issue, but worth noting and adjusting in the future.
    def load_distance_graph(self, file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            # Skip the first line (header row)
            header = lines[0].strip().split(",")[1:]  # Exclude the first column
            for line in lines[1:]:  # Start from the second line
                data = line.strip().split(",")
                from_node = data[0]  # First column is the 'from' node
                for i, to_node in enumerate(header):
                    if i + 1 < len(data):  # Ensure we don't go out of bounds
                        distance = float(data[i + 1])
                        self.add_edge(from_node, to_node, distance)
