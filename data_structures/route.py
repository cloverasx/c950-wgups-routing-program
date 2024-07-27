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
    def has_deadline_failures(truck, packages=None):
        if packages:
            return Route._check_for_failures(truck, packages)
        if not truck.packages:
            return False
        return Route._check_for_failures(truck, truck.packages)

    @staticmethod
    def _check_for_failures(truck, packages):
        current_time = truck.current_time
        location = truck.current_location
        for package in packages:
            distance = Route.distance_graph.get_distance(location, package.address)
            travel_time = distance / truck.speed
            delivery_time = (
                datetime.datetime.combine(datetime.date.today(), current_time)
                + datetime.timedelta(hours=travel_time)
            ).time()
            if delivery_time > package.deadline:
                return True
            current_time = delivery_time
            location = package.address
        return False

    @staticmethod
    def _is_package_on_truck(package):
        return package.status.startswith("on truck")

    @staticmethod
    def _update_delayed_packages(packages, current_time):
        for package in packages:
            if package.is_delayed(current_time):
                package.status = "delayed"

    @staticmethod
    def get_available_packages(packages, current_time, truck=None):
        if truck:
            return [
                p
                for p in packages
                if not p.is_delayed(current_time)
                and not p.is_on_truck()
                and not p.is_delivered()
                and Route._can_deliver_on_truck(p, truck)
            ]
        return [
            p
            for p in packages
            if not p.is_delayed(current_time)
            and not p.is_on_truck()
            and not p.is_delivered()
        ]

    @staticmethod
    def sort_by_deadline(packages):
        return sorted(packages, key=lambda p: p.deadline)

    @staticmethod
    def show_route(truck):
        route = []
        current_time = truck.current_time
        location = truck.current_location
        for package in truck.packages:
            distance = Route.distance_graph.get_distance(location, package.address)
            travel_time = distance / truck.speed
            delivery_time = (
                datetime.datetime.combine(datetime.date.today(), current_time)
                + datetime.timedelta(hours=travel_time)
            ).time()
            late = delivery_time > package.deadline
            route.append(
                f"Package {package.id} to {package.address} by {delivery_time}. {'LATE' if late else ''}"
            )
            current_time = delivery_time
            location = package.address
        return route

    @staticmethod
    def is_grouped_in_list(group_packages, package_list):
        for group in group_packages:
            group_in_trimmed = [pkg for pkg in group if pkg in package_list]
            return group_in_trimmed
        return False

    @staticmethod
    def add_group_remainder(group_packages, package_list):
        for group in group_packages:
            if set(group).issubset(set(package_list)):
                continue
            else:
                remaining_group = [pkg for pkg in group if pkg not in package_list]
                for i in range(len(package_list) - 1, -1, -1):
                    if len(remaining_group) == 0:
                        break

                    if package_list[i] not in group:
                        package_list[i] = remaining_group.pop(0)
                package_list.extend(remaining_group)
            # remove all packages from group
            group.clear()


class RoutePlanner:
    @staticmethod
    def plan_routes(packages, trucks, current_time):
        # debug:
        print(Route.distance_graph)

        # update delayed packages
        Route._update_delayed_packages(packages, current_time)

        # assign packages to trucks
        for truck in trucks:
            RoutePlanner._assign_packages_to_truck(
                truck,
                packages,
                current_time,
            )

        # debug:
        for truck in trucks:
            # id_list = [p.id for p in truck.packages]
            print(f"Truck {truck.id} package list: {[p.id for p in truck.packages]}")

        for t in trucks:
            print(f"\nTruck {t.id} route:")
            for _ in Route.show_route(t):
                print(_)

    @staticmethod
    def _assign_packages_to_truck(
        truck,
        all_packages,
        current_time,
    ):
        available_packages = Route.get_available_packages(
            all_packages, current_time, truck
        )
        group_packages = Route.get_group_packages(all_packages, current_time)

        # debug:
        print(f"available packages: {[p.id for p in available_packages]}")

        # sort by deadline
        priority_packages = Route.sort_by_deadline(available_packages)

        selected_packages = []
        for package in priority_packages:
            if len(selected_packages) >= truck.capacity:
                break
            for group in group_packages:
                if (
                    package in group
                    and len(selected_packages) + len(group_packages) > truck.capacity
                ):
                    test_packages = selected_packages + group
                    if not Route.has_deadline_failures(truck, test_packages):
                        selected_packages.extend(group)
                        group.clear()
                        continue
            else:
                test_packages = selected_packages + [package]
                if not Route.has_deadline_failures(truck, test_packages):
                    selected_packages.append(package)

        print(truck.current_time)
        print(truck.next_delivery_time)

        RoutePlanner._load_packages(truck, selected_packages)

    @staticmethod
    def _load_packages(truck, packages):
        for package in packages:
            package.status = f"on truck {truck.id}"
            truck.load_package(package)

    @staticmethod
    def remove_packages(truck, packages):
        for package in packages:
            package.status = "at hub"
            truck.remove_package(package)

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
                        and Route.has_deadline_failures(
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
