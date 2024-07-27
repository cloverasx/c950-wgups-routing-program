from data_structures.truck import Truck
from data_structures.hash_table import HashTable
from data_structures.graph import Graph
from data_structures.truck_driver import TruckDriver
from data_structures.route import Route, RoutePlanner
import config
import time

import datetime


class SimulationClock:
    def __init__(self):
        self.time_scale = config.TIME_SCALE
        self.current_time = config.START_TIME

    def advance(self, delta):
        self.current_time += delta * self.time_scale

    def get_time(self):
        return self.current_time


class DeliverySimulation:
    def __init__(self):
        self.clock = SimulationClock()
        self.events = []

        self.current_time = datetime.time(8, 0)  # Start at 8:00 AM
        self.package_table = HashTable()
        self.distance_graph = None
        self.trucks = []
        self.truck_drivers = []
        self.packages_at_hub = False
        self.algorithm = config.ALGORITHM

        # Load package and distance data from spreadsheets
        self._load_package_data(config.PACKAGE_FILE_CSV)
        self._load_distance_data(config.DISTANCE_FILE_CSV)
        self._initialize_trucks()
        self._initialize_truck_drivers()
        Route.set_algorithm(self.algorithm)
        Route.set_graph(self.distance_graph)
        Truck.set_graph(self.distance_graph)

    def run_step(self):
        # process next event, update state
        self.clock.advance(1)
        # placeholder: update some state
        return f"Time: {self.clock.get_time():.2f}, Packages Delivered: {int(self.clock.get_time())}"

    def get_status(self):
        return f"Time: {self.clock.get_time():.2f}"

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

    def _plan_route(self):
        RoutePlanner.plan_routes(self.package_table, self.trucks, self.current_time)

        # debug:
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
            self._deliver_packages()
            self._update_time()

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
        pass

    def _update_time(self):
        pass

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
