from data_structures.truck import Truck
from data_structures.hash_table import HashTable
from data_structures.graph import Graph
from data_structures.truck_driver import TruckDriver
from data_structures.route import Route, RoutePlanner
import config
import time

import datetime


class DeliverySimulation:
    def __init__(self, package_file, distance_file):
        self.current_time = datetime.time(8, 0)  # Start at 8:00 AM
        self.package_table = HashTable()
        self.distance_graph = None
        self.trucks = []
        self.truck_drivers = []
        self.packages_at_hub = False
        self.algorithm = config.ALGORITHM

        # Load package and distance data from spreadsheets
        self._load_package_data(package_file)
        self._load_distance_data(distance_file)
        self._initialize_trucks()
        self._initialize_truck_drivers()
        Route.set_algorithm(self.algorithm)
        Route.set_graph(self.distance_graph)
        Truck.set_graph(self.distance_graph)

    def _get_current_time(self):
        return self.current_time

    def _load_package_data(self, file_path):
        self.package_table = HashTable(file_path)
        if len(self.package_table) > 0:
            self.packages_at_hub = True

    def _load_distance_data(self, file_path):
        self.distance_graph = Graph(file_path)

    def _initialize_trucks(self):
        # Create 3 trucks as per the scenario
        for i in range(1, config.TRUCK_COUNT + 1):
            self.trucks.append(
                Truck(
                    id=i,
                    capacity=config.TRUCK_CAPACITY,
                    speed=config.TRUCK_SPEED,
                    current_time=self._get_current_time(),
                )
            )

    def _initialize_truck_drivers(self):
        # Create 2 drivers as per the scenario
        for i in range(1, config.DRIVER_COUNT + 1):
            self.truck_drivers.append(TruckDriver(id=i))

    # TODO: Implement route planning logic
    def _plan_route(self):
        RoutePlanner.plan_routes(self.package_table, self.trucks, self.current_time)
        for truck in self.trucks:
            print(f"Truck {truck.id} package list:")
            for package in truck.packages:
                print(f"PID {package.id}")

        print()

    def _add_package_with_wrong_address(self):
        package_9 = self.package_table.lookup(9)
        package_9.note = "delayed until 10:20 am"
        self.package_table.insert(9, package_9)

    def run_simulation(self):
        # specifically handle package 9 for wrong address
        # update package.note to include a delay until 10:20 am
        self._add_package_with_wrong_address()
        while self.packages_at_hub or any(truck.packages for truck in self.trucks):
            self._plan_route()
            self._load_trucks()
            self._deliver_packages()
            self._update_time()

    def _load_trucks(self):
        #### I'M HERE ####
        # THIS NEEDS TO ROUTE BASED ON TWO DRIVERS BEING AVAILABLE AT THE SAME TIME FIRST
        # ACTUALLY DO THE PLAN ROUTE FIRST**
        ##################

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
