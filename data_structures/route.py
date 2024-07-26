# from utils.string_utils import StringUtils as su
import config

# from datetime import datetime, timedelta, date
import datetime
import copy
# from abc import ABC


class Route:
    algorithm = None
    distance_graph = None

    @classmethod
    def set_algorithm(cls, algorithm_name):
        if algorithm_name.lower() == "nearest_neighbor":
            cls.algorithm = NearestNeighbor
        else:
            raise ValueError("Invalid algorithm name")

    @classmethod
    def set_graph(cls, graph):
        cls.distance_graph = graph
        NearestNeighbor.set_graph(graph)

    @classmethod
    def route(cls, *args, **kwargs):
        if cls.algorithm:
            return cls.algorithm.route(*args, **kwargs)
        else:
            raise ValueError("Algorithm not set")

    @staticmethod
    def get_priority_packages(packages, current_time):
        priority_packages = []
        for package in packages:
            if (
                not package.is_delayed(current_time)
                and package.has_deadline()
                and not package.is_on_truck()
                and not package.is_delivered()
            ):
                priority_packages.append(package)
        return priority_packages

    @staticmethod
    def get_delayed_packages(current_time, packages):
        delayed_packages = []

        print(current_time)

        for package in packages:
            if (
                package.is_delayed(current_time)
                and not package.is_on_truck()
                and not package.is_delivered()
            ):
                delayed_packages.append(package)
        return delayed_packages

    @staticmethod
    def get_group_packages(packages, current_time):
        grouped_packages = []
        # package_to_group = {}

        for package in packages:
            if (
                package.is_in_group()
                and not package.is_on_truck()
                and not package.is_delayed(current_time)
                and not package.is_delivered()
            ):
                group = [package]
                related_ids = [int(s) for s in package.note.split() if s.isdigit()]
                for pid in related_ids:
                    related_package = packages.lookup(pid)
                    group.append(related_package)

                grouped_packages.append(group)

        # consolidate groups with shared packages
        for group in grouped_packages:
            for package in group:
                # if package in any other group, merge the groups
                for other_group in grouped_packages:
                    if package in other_group and group != other_group:
                        # only append packages not already in the group
                        for other_package in other_group:
                            if other_package not in group:
                                group.append(other_package)
                        grouped_packages.remove(other_group)
        return grouped_packages

    @staticmethod
    def get_truck_specific_packages(packages, truck_number=None):
        group = []
        if truck_number:
            for package in packages:
                note = package.note.lower()
                if "truck" in note:
                    parsed_truck_number = Route._parse_truck_number(note)
                    if parsed_truck_number == truck_number:
                        group.append(package)
        else:
            for package in packages:
                note = package.note.lower()
                if "truck" in note:
                    group.append(package)

        return group

    @staticmethod
    def _can_deliver_on_truck(package, truck):
        if "truck" in package.note.lower():
            parsed_truck_number = Route._parse_truck_number(package.note)
            if parsed_truck_number == truck.id:
                return True
            else:
                return False
        return True

    @staticmethod
    def _parse_truck_number(note):
        words = note.split()
        for i, word in enumerate(words):
            if word == "truck" and i + 1 < len(words):
                return int("".join(filter(str.isdigit, words[i + 1])))

    @staticmethod
    def _get_temp_route(truck):
        if not truck.packages:
            return []
        t = copy.deepcopy(truck)
        if not t.current_location:
            t.location = config.HUB_LOCATION
        for package in Route.route(t.packages, t.current_location):
            t.load_package(package)
        return t

    @staticmethod
    def has_no_deadline_failures(truck):
        if not truck.packages:
            return True
        current_time = truck.next_delivery_time
        location = truck.current_location
        for package in truck.packages:
            distance = Route.distance_graph.get_distance(location, package.address)
            travel_time = distance / truck.speed
            delivery_time = (
                datetime.datetime.combine(datetime.date.today(), current_time)
                + datetime.timedelta(hours=travel_time)
            ).time()
            if delivery_time > package.deadline:
                return False
            current_time = delivery_time
            location = package.address
        return True

    @staticmethod
    def _is_package_on_truck(package):
        return package.status.startswith("on truck")

    @staticmethod
    def _update_delayed_packages(packages, current_time):
        for package in packages:
            if package.is_delayed(current_time):
                package.status = "delayed"


class RoutePlanner:
    @staticmethod
    def plan_routes(packages, trucks, current_time):
        # debug:
        print(Route.distance_graph)

        # assign packages to trucks
        for truck in trucks:
            # update delayed packages
            Route._update_delayed_packages(packages, current_time)
            # group packages by priority, delayed, and truck-specific
            priority_packages = Route.get_priority_packages(packages, current_time)
            group_packages = Route.get_group_packages(packages, current_time)
            delayed_packages = Route.get_delayed_packages(current_time, packages)

            RoutePlanner._assign_packages_to_truck(
                truck,
                priority_packages,
                delayed_packages,
                group_packages,
                packages,
                current_time,
            )

        # debug:
        for truck in trucks:
            # id_list = [p.id for p in truck.packages]
            print(f"Truck {truck.id} package list: {[p.id for p in truck.packages]}")

        # optimize routes
        for truck in trucks:
            t = copy.deepcopy(truck)
            truck.packages = []
            optimized_route = Route.route(t.packages, t.current_location)
            for package in optimized_route:
                truck.load_package(package)

        # check and adjust for missed deadlines
        RoutePlanner._adjust_for_deadlines(trucks)

    @staticmethod
    def _assign_packages_to_truck(
        truck,
        priority_packages,
        delayed_packages,
        group_packages,
        all_packages,
        current_time,
    ):
        # start with priority packages
        available_packages = [
            p
            for p in priority_packages
            if p not in delayed_packages and Route._can_deliver_on_truck(p, truck)
        ]

        # debug:
        print("available packages:")
        for package in available_packages:
            print(package.id)

        RoutePlanner._load_packages(
            truck, RoutePlanner._select_packages(available_packages, truck.capacity)
        )

        ## add grouped packages
        for group in group_packages:
            # check to see if any of the group members are already on the truck
            if any(p in truck.packages for p in group):
                # if all the group packages are on the truck, skip
                if all(p in group for p in truck.packages):
                    continue
                else:
                    if (
                        truck.capacity - len(truck.packages) >= len(group)
                        and all(Route._can_deliver_on_truck(p, truck) for p in group)
                        and all(p not in delayed_packages for p in group)
                    ):
                        # Load the entire group on the truck
                        group_remainder = [p for p in group if p not in truck.packages]
                        RoutePlanner._load_packages(truck, group_remainder)

            available_group = [p for p in group if p not in truck.packages]
            if all(
                Route._can_deliver_on_truck(p, truck) for p in available_group
            ) and len(group) <= (truck.capacity - len(truck.packages)):
                RoutePlanner._load_packages(truck, available_group)

        # fill remaining capacity
        remaining_packages = [
            p
            for p in all_packages
            if p not in truck.packages
            and Route._can_deliver_on_truck(p, truck)
            and not p.is_delayed(current_time)
            and not p.is_in_group()
            and not p.is_delivered()
        ]
        RoutePlanner._load_packages(
            truck,
            RoutePlanner._select_packages(
                remaining_packages, truck.capacity - len(truck.packages)
            ),
        )

    @staticmethod
    def _select_packages(packages, capacity):
        return sorted(packages, key=lambda p: p.deadline)[:capacity]

    @staticmethod
    def _load_packages(truck, packages):
        for package in packages:
            package.status = f"on truck {truck.id}"
            truck.load_package(package)

    @staticmethod
    def _adjust_for_deadlines(trucks):
        for i, truck in enumerate(trucks):
            current_time = truck.next_delivery_time
            location = truck.current_location
            for j, package in enumerate(truck.packages):
                distance = Route.distance_graph.get_distance(location, package.address)
                travel_time = distance / truck.speed
                delivery_time = (
                    datetime.datetime.combine(datetime.date.today(), current_time)
                    + datetime.timedelta(hours=travel_time)
                ).time()
                # if delivery_time > datetime.strptime.(package.deadline, "%H:%M:%S").time():
                if delivery_time > package.deadline:
                    # swap package with another trucks package if available
                    RoutePlanner._swap_packages(trucks, i, j)
                current_time = delivery_time
                location = package.address

    @staticmethod
    def _swap_packages(trucks, current_truck_index, package_index):
        current_truck = trucks[current_truck_index]
        package = current_truck.packages[package_index]
        for other_truck_index, other_truck in enumerate(trucks):
            if other_truck_index != current_truck_index:
                for other_package_index, other_package in enumerate(
                    other_truck.packages
                ):
                    if (
                        other_package.deadline > package.deadline
                        and Route._can_deliver_on_truck(other_package, current_truck)
                        and Route._can_deliver_on_truck(package, other_truck)
                        and Route.has_no_deadline_failures(
                            Route._get_temp_route(other_truck)
                        )
                    ):
                        # swap packages
                        current_truck.packages[package_index] = other_package
                        other_truck.packages[other_package_index] = package
                        return True
        return False


class NearestNeighbor:
    distance_graph = None

    @classmethod
    def set_graph(cls, graph):
        cls.distance_graph = graph

    def _update_deliverable_packages(self):
        self.deliverable = self.undelivered - self.delayed_packages
        for pid in self.delayed_packages:
            if self._is_package_deliverable(pid):
                self.deliverable.add(pid)

    def _is_package_deliverable(self, package_id):
        package = self.packages.lookup(package_id)
        if "delayed" in package.note.lower():
            delayed_time = self._parse_delay_time(package.note)
            return self.current_time > delayed_time
        return True

    def _parse_delay_time(self, note):
        time_str = note.split("until ")[-1].strip()
        # Remove the 'am' or 'pm' and split into hours and minutes
        time_parts = time_str[:-2].split(":")
        hours = int(time_parts[0])
        minutes = int(time_parts[1])

        # Adjust hours for PM times
        if time_str.lower().endswith("pm") and hours != 12:
            hours += 12
        elif time_str.lower().endswith("am") and hours == 12:
            hours = 0

        # Create a time object
        return datetime.time(hours, minutes)

    def _update_route(self, package_id):
        package = self.packages.lookup(package_id)
        distance_to_next = self.graph.get_distance(
            self.current_location, package.address
        )

        route_entry = [
            package_id,
            package.address,
            distance_to_next,
            self.total_distance + distance_to_next,
        ]

        self.route_list.append(route_entry)
        self.total_distance += distance_to_next

    def _return_to_hub(self):
        distance_to_hub = self.graph.get_distance(self.current_location, self.hub)

        hub_entry = [
            "Hub",
            self.hub,
            distance_to_hub,
            self.total_distance + distance_to_hub,
        ]

        self.total_distance += distance_to_hub
        self.route_list.append(hub_entry)

    @staticmethod
    def _find_nearest_package(packages, location, graph):
        # set the first package in packages as 'nearest'
        nearest_package = packages[0]
        for package in packages:
            if NearestNeighbor.distance_graph.get_distance(
                location, package.address
            ) < NearestNeighbor.distance_graph.get_distance(
                location, nearest_package.address
            ):
                nearest_package = package
        return nearest_package

    def _get_current_time(self):
        return datetime.time(8, 0)

    def get_total_distance(self):
        return self.total_distance

    @staticmethod
    def route(packages, location):
        unrouted = packages.copy()  # Create a copy of the packages list
        routed = []
        while unrouted:
            nearest_package = NearestNeighbor._find_nearest_package(
                unrouted, location, NearestNeighbor.distance_graph
            )
            routed.append(nearest_package)
            location = nearest_package.address
            unrouted.remove(nearest_package)

        return routed
