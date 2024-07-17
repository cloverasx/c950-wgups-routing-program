import datetime


class NearestNeighbor:
    def __init__(self, graph, packages, hub=None):
        self.graph = graph
        self.packages = packages
        self.hub = hub or "4001 south 700 east"
        self.route_list = []
        self.total_distance = 0
        self.drivers = 2
        self.current_time = self._get_current_time()
        self.current_location = self.hub

        # Organize package categories
        self.all_package_ids = set(self.packages.get_all_ids())
        self.undelivered = set(self.all_package_ids)
        self.deliverable = set()
        self.packages_with_deadlines = set()
        self.delayed_packages = set()
        self.truck_specific_packages = {}
        self.tandem_required_packages = []

        self._initialize_package_categories()

    def _initialize_package_categories(self):
        self._categorize_packages_with_deadlines()
        self._categorize_delayed_packages()
        self._categorize_truck_specific_packages()
        self._categorize_tandem_required_packages()
        self._update_deliverable_packages()

    def _categorize_packages_with_deadlines(self):
        self.packages_with_deadlines = {
            pid
            for pid in self.all_package_ids
            if self.packages.lookup(pid).deadline
            and self.packages.lookup(pid).deadline != "eod"
        }

    def _categorize_delayed_packages(self):
        self.delayed_packages = {
            pid
            for pid in self.all_package_ids
            if "delayed" in self.packages.lookup(pid).note.lower()
        }

    def _categorize_truck_specific_packages(self):
        for pid in self.all_package_ids:
            package = self.packages.lookup(pid)
            note = package.note.lower()
            if "truck" in note:
                words = note.split()
                for i, word in enumerate(words):
                    if word == "truck" and i + 1 < len(words):
                        try:
                            truck_number = int(
                                "".join(filter(str.isdigit, words[i + 1]))
                            )
                            self.truck_specific_packages.setdefault(
                                truck_number, set()
                            ).add(pid)
                            break
                        except ValueError:
                            continue

    def _categorize_tandem_required_packages(self):
        tandem_required_package_groups = []
        package_to_group = {}

        for package_id in self.all_package_ids:
            package = self.packages.lookup(package_id)
            if "delivered with" in package.note.lower():
                related_ids = [int(s) for s in package.note.split() if s.isdigit()]
                related_ids.append(package_id)

                existing_groups = set(
                    package_to_group.get(pid, -1)
                    for pid in related_ids
                    if pid in package_to_group
                )

                if existing_groups:
                    # Merge existing groups
                    target_group = min(existing_groups)
                    for group_index in existing_groups:
                        if group_index != target_group:
                            tandem_required_package_groups[target_group].extend(
                                tandem_required_package_groups[group_index]
                            )
                            tandem_required_package_groups[group_index] = None

                    tandem_required_package_groups[target_group].extend(
                        [
                            pid
                            for pid in related_ids
                            if pid not in tandem_required_package_groups[target_group]
                        ]
                    )
                    for pid in related_ids:
                        package_to_group[pid] = target_group
                else:
                    # Create a new group
                    new_group = list(set(related_ids))
                    tandem_required_package_groups.append(new_group)
                    for pid in new_group:
                        package_to_group[pid] = len(tandem_required_package_groups) - 1

        # Remove None entries and deduplicate
        tandem_required_package_groups = [
            list(set(group))
            for group in tandem_required_package_groups
            if group is not None
        ]

        return tandem_required_package_groups

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

    def route(self):
        while self.deliverable:
            prioritized_packages = self.deliverable & self.packages_with_deadlines
            if not prioritized_packages:
                prioritized_packages = self.deliverable

            nearest_package_id = self._find_nearest_package(
                self.current_location, prioritized_packages
            )
            self._update_route(nearest_package_id)
            self.current_location = self.packages.lookup(nearest_package_id).address
            self.deliverable.remove(nearest_package_id)
            self.undelivered.remove(nearest_package_id)

        self._return_to_hub()
        return self.route_list

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

    def _find_nearest_package(self, current_location, package_ids):
        return min(
            package_ids,
            key=lambda pid: self.graph.get_distance(
                current_location, self.packages.lookup(pid).address
            ),
        )

    def _get_current_time(self):
        return datetime.time(8, 0)

    def get_total_distance(self):
        return self.total_distance
