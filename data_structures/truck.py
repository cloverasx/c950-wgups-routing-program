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
