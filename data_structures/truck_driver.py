import config


class TruckDriver:
    def __init__(self, id):
        self.id = id
        self.is_driving = False
        self.location = config.HUB_LOCATION
        self.route = []

    def assign_route(self, route):
        self.route = route
