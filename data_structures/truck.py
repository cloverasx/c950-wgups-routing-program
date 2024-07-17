from data_structures.package import Package
from utils.graph_utils import GraphUtils
from data_structures.graph import Graph
import datetime


class Truck:
    def __init__(self, capacity, speed):
        self.capacity = capacity
        self.speed = speed
        self.packages = []
        self.current_location = "4300 s 1300 e"  # HUB location
        self.distance_graph = None

        self.current_time = datetime.time(8, 0)

    def load_package(self, package):
        self.packages.append(package)
        self.distance_graph = GraphUtils.load_distance_graph("data/distance_table.csv")

    def deliver_packages(self):
        for package in self.packages:
            self._drive_to(package)

    def _drive_to(self, package):
        location = package.address
        delivery_time = self._calculate_delivery_time(location)
        package.deliver(f"Delivered at {delivery_time}")
        # debug: print each location status
        print(f"Package {package.id} delivered at {delivery_time}")

    def _calculate_delivery_time(self, location):
        distance = self.distance_graph.get_distance(self.current_location, location)
        # get the time to reach location
        time_delta = datetime.timedelta(hours=distance / self.speed)
        delivery_time = (
            datetime.datetime.combine(datetime.date.today(), self.current_time)
            + time_delta
        ).time()
        self.current_time = delivery_time
        return delivery_time
