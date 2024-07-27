from data_structures.package import Package
from data_structures.graph import Graph
from data_structures.route import Route
import config
import datetime


class Truck:
    def __init__(self, id, capacity, speed, current_time):
        self.id = id
        self.capacity = capacity
        self.speed = speed
        self.packages = []
        self.delivered_packages = []
        self.current_location = config.HUB_LOCATION
        self.total_mileage = 0
        self.next_delivery_time = None
        self.is_driving = False
        self.driver = None
        self.distance_graph = None
        self.current_time = current_time

    @classmethod
    def set_graph(cls, graph):
        cls.distance_graph = graph

    def assign_driver(self, driver):
        self.driver = driver

    def load_package(self, package):
        self.packages.append(package)
        # if self.packages:
        #     self.next_delivery_time = self._calculate_delivery_time(
        #         self.packages[0].address
        #     )

    def remove_package(self, package):
        self.packages.remove(package)

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
        distance = Route.distance_graph.get_distance(self.current_location, location)
        # get the time to reach location
        time_delta = datetime.timedelta(hours=distance / self.speed)
        delivery_time = (
            datetime.datetime.combine(datetime.date.today(), self.current_time)
            + time_delta
        ).time()
        self.current_time = delivery_time
        return delivery_time

    def begin_route(self):
        self.is_driving = True
        self.next_delivery_time = self._calculate_delivery_time(
            self.packages[0].address
        )
