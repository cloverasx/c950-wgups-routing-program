class RoutingAlgorithm:
    def __init__(self, packages, distance_table):
        self.packages = packages
        self.distance_table = distance_table

    def optimize_route(self):
        pass

    def calculate_total_distance(self):
        pass
    

class Truck:
    def __init__(self, capacity, speed):
        self.capacity = capacity
        self.speed = speed
        self.packages = []
        self.current_location = "HUB"

    def load_package(self, package):
        self.packages.append(package)

    def deliver_packages(self):
        pass