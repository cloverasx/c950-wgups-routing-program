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
        self.hub = hub if hub is not None else "4001 south 700 east"
        self.route_list = []
        self.total_distance = 0
        # empty verbose route dict including the package id, address, and distance from
        # the previous location
        self.route_dict = {}

    def route(self):
        undelivered = deque(self.packages.get_all_ids())
        current_location = self.hub

        while undelivered:
            # Find the nearest package
            nearest_package_id = min(
                undelivered,
                key=lambda pid: self.graph.get_distance(
                    current_location, self.packages.lookup(pid).address
                ),
            )

            # add pid, address, and distance to the route dict
            self.route_dict[nearest_package_id] = {
                "pid": nearest_package_id,
                "address": self.packages.lookup(nearest_package_id).address,
                "distance": self.graph.get_distance(
                    current_location, self.packages.lookup(nearest_package_id).address
                ),
                "cumulative_distance": self.total_distance
                + self.graph.get_distance(
                    current_location, self.packages.lookup(nearest_package_id).address
                ),
            }

            # Move to the nearest package
            nearest_package = self.packages.lookup(nearest_package_id)
            distance_to_next = self.graph.get_distance(
                current_location, nearest_package.address
            )

            # Update route and distance
            self.route_list.append((nearest_package_id, nearest_package.address))
            self.total_distance += distance_to_next

            # debug: catch end of route
            if nearest_package_id == 11:
                pass

            # Update current location and remove package from undelivered
            current_location = nearest_package.address
            undelivered.remove(nearest_package_id)

        # add hub to route dict
        self.route_dict["Hub"] = {
            "pid": "Hub",
            "address": self.hub,
            "distance": self.graph.get_distance(current_location, self.hub),
            "cumulative_distance": self.total_distance
            + self.graph.get_distance(current_location, self.hub),
        }

        # Return to hub
        self.total_distance += self.graph.get_distance(current_location, self.hub)
        self.route_list.append(("Return", self.hub))

        # Return the route
        return self.route_list, self.route_dict

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
