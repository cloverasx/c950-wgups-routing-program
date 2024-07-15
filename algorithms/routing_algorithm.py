from abc import ABC, abstractmethod
from collections import deque


class RoutingAlgorithm(ABC):
    def __init__(self, distance_graph, packages):
        self.distance_table = distance_graph
        self.packages = packages

    @abstractmethod
    def route(self):
        pass

    @abstractmethod
    def get_total_distance(self):
        pass


class NearestNeighbor(RoutingAlgorithm):
    def __init__(self, graph, packages, hub=None):
        super().__init__(graph, packages)
        self.graph = graph
        self.packages = packages
        self.hub = hub or "4001 south 700 east"
        self.route_list = []
        self.route_dict = {}
        self.total_distance = 0

    def route(self):
        undelivered = deque(self.packages.get_all_ids())
        current_location = self.hub

        while undelivered:
            nearest_package_id = self._find_nearest_package(
                current_location, undelivered
            )
            self._update_route(nearest_package_id, current_location)
            current_location = self.packages.lookup(nearest_package_id).address
            undelivered.remove(nearest_package_id)

        self._return_to_hub(current_location)
        return self.route_list, self.route_dict

    def _find_nearest_package(self, current_location, undelivered):
        return min(
            undelivered,
            key=lambda pid: self.graph.get_distance(
                current_location, self.packages.lookup(pid).address
            ),
        )

    def _update_route(self, package_id, current_location):
        package = self.packages.lookup(package_id)
        distance_to_next = self.graph.get_distance(current_location, package.address)

        self.route_dict[package_id] = {
            "pid": package_id,
            "address": package.address,
            "distance": distance_to_next,
            "cumulative_distance": self.total_distance + distance_to_next,
        }

        self.route_list.append((package_id, package.address))
        self.total_distance += distance_to_next

    def _return_to_hub(self, current_location):
        distance_to_hub = self.graph.get_distance(current_location, self.hub)

        self.route_dict["Hub"] = {
            "pid": "Hub",
            "address": self.hub,
            "distance": distance_to_hub,
            "cumulative_distance": self.total_distance + distance_to_hub,
        }

        self.total_distance += distance_to_hub
        self.route_list.append(("Return", self.hub))

    def get_total_distance(self):
        return self.total_distance


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
