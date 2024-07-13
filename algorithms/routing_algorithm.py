from abc import ABC, abstractmethod


class RoutingAlgorithm(ABC):
    def __init__(self, packages, distance_graph):
        self.packages = packages
        self.distance_table = distance_graph

    @abstractmethod
    def route(self):
        pass

    @abstractmethod
    def get_total_distance(self):
        pass


class NearestNeighbor(RoutingAlgorithm):
    def __init__(self, packages, distance_graph):
        super().__init__(packages, distance_graph)
        self.distance_table = distance_graph
        self.packages = packages
        self.route()

    # TODO: Implement the Nearest Neighbor algorithm
    def route(self):
        pass

    def get_total_distance(self):
        pass


class GreedyAlgorithm(RoutingAlgorithm):
    def __init__(self, packages, distance_graph):
        super().__init__(packages, distance_graph)
        self.distance_table = distance_graph
        self.packages = packages
        self.route()

    # TODO: Implement the Greedy Algorithm
    def route(self):
        pass

    def get_total_distance(self):
        pass


def compare_algorithms(packages, graph, algorithms):
    results = []
    for AlgorithmClass in algorithms:
        algorithm = AlgorithmClass(packages, graph)
        route = algorithm.route()
        distance = algorithm.get_total_distance()
        results.append(
            {"algorithm": AlgorithmClass.__name__, "route": route, "distance": distance}
        )
    return results
