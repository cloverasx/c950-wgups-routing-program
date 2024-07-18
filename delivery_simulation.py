from data_structures.truck import Truck
from data_structures.hash_table import HashTable
from utils.data_hashing_utils import DataHashingUtils
from utils.graph_utils import GraphUtils

import datetime


class DeliverySimulation:
    def __init__(self, package_file, distance_file):
        self.current_time = datetime.time(8, 0)  # Start at 8:00 AM
        self.package_table = HashTable()
        self.distance_graph = None
        self.trucks = []
        self.packages_at_hub = set()
        self.delivered_packages = set()

        self._load_package_data(package_file)
        self._load_distance_data(distance_file)
        self._initialize_trucks()

    def _load_package_data(self, file_path):
        packages = DataHashingUtils.load_package_data(file_path)
        for package in packages:
            self.package_table.insert(package.id, package)
            self.packages_at_hub.add(package.id)

    def _load_distance_data(self, file_path):
        self.distance_graph = GraphUtils.load_distance_graph(file_path)

    def _initialize_trucks(self):
        # Create 3 trucks as per the scenario
        for _ in range(3):
            self.trucks.append(Truck(16, 18))  # 16 package capacity, 18 mph speed

    def run_simulation(self):
        while self.packages_at_hub or any(truck.packages for truck in self.trucks):
            self._load_trucks()
            self._deliver_packages()
            self._update_time()

    def _load_trucks(self):
        for truck in self.trucks:
            if not truck.is_full() and not truck.is_en_route:
                available_packages = self._get_available_packages()
                selected_packages = self._select_packages_for_truck(
                    truck, available_packages
                )
                for package_id in selected_packages:
                    package = self.package_table.lookup(package_id)
                    truck.load_package(package)
                    self.packages_at_hub.remove(package_id)

    def _get_available_packages(self):
        return [
            pid
            for pid in self.packages_at_hub
            if self._is_package_available(self.package_table.lookup(pid))
        ]

    def _is_package_available(self, package):
        if "delayed" in package.note.lower():
            delay_time = self._parse_delay_time(package.note)
            return self.current_time >= delay_time
        return True

    def _select_packages_for_truck(self, truck, available_packages):
        # Implement package selection logic (e.g., based on deadlines, special notes)
        # This is where you'd use your routing algorithm
        return []  # Placeholder

    def _deliver_packages(self):
        for truck in self.trucks:
            if truck.packages:
                truck.deliver_packages(self.distance_graph, self.current_time)
                self.delivered_packages.update(truck.delivered_packages)
                truck.delivered_packages.clear()

    def _update_time(self):
        # Increment time based on the fastest truck's next delivery
        # This is a simplified time update mechanism
        self.current_time = min(
            truck.next_delivery_time
            for truck in self.trucks
            if truck.next_delivery_time
        )

    def get_package_status(self, package_id, time):
        package = self.package_table.lookup(package_id)
        if package.id in self.delivered_packages:
            return f"Delivered at {package.delivery_time}"
        elif any(package.id in truck.packages for truck in self.trucks):
            return "En route"
        else:
            return "At the hub"

    def get_total_mileage(self):
        return sum(truck.total_mileage for truck in self.trucks)
