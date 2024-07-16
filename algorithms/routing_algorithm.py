from collections import deque


class NearestNeighbor:
    def __init__(self, graph, packages, hub=None):
        self.graph = graph
        self.packages = packages
        self.hub = hub or "4001 south 700 east"
        self.route_list = []
        self.total_distance = 0

    def route(self):
        undelivered = deque(self.packages.get_all_ids())

        # get delivery deadlines and sort for priority
        undelivered_with_deadlines, undelivered_without_deadlines = (
            self._get_package_deadlines(undelivered)
        )

        current_location = self.hub

        while undelivered:
            nearest_package_id = self._find_nearest_package(
                current_location, undelivered
            )
            self._update_route(nearest_package_id, current_location)
            current_location = self.packages.lookup(nearest_package_id).address
            undelivered.remove(nearest_package_id)

        self._return_to_hub(current_location)
        return self.route_list

    def get_total_distance(self):
        return self.total_distance

    def _get_package_deadlines(self, undelivered):
        undelivered_with_deadlines = []
        undelivered_without_deadlines = []
        for package_id in undelivered:
            package = self.packages.lookup(package_id)
            if package.deadline:
                if package.deadline == "eod":
                    undelivered_without_deadlines.append(package_id)
                else:
                    undelivered_with_deadlines.append(package_id)
            else:
                undelivered_without_deadlines.append(package_id)
        return undelivered_with_deadlines, undelivered_without_deadlines

    def _update_route(self, package_id, current_location):
        package = self.packages.lookup(package_id)
        distance_to_next = self.graph.get_distance(current_location, package.address)

        route_entry = [
            package_id,
            package.address,
            distance_to_next,
            self.total_distance + distance_to_next,
        ]

        self.route_list.append(route_entry)
        self.total_distance += distance_to_next

    def _return_to_hub(self, current_location):
        distance_to_hub = self.graph.get_distance(current_location, self.hub)

        hub_entry = [
            "Hub",
            self.hub,
            distance_to_hub,
            self.total_distance + distance_to_hub,
        ]

        self.total_distance += distance_to_hub
        self.route_list.append(hub_entry)

    def _find_nearest_package(self, current_location, undelivered):
        return min(
            undelivered,
            key=lambda pid: self.graph.get_distance(
                current_location, self.packages.lookup(pid).address
            ),
        )
