from data_structures.graph import Graph


# This class doubles the necessary data and should be optimized to only have one
# instance of each node-edge-node relationship since they're symmetric. This isn't
# a critical issue, but worth noting and adjusting in the future.
class GraphUtils:
    @staticmethod
    def load_distance_graph(file_path):
        distance_graph = Graph()
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
                        distance_graph.add_edge(from_node, to_node, distance)
        return distance_graph
