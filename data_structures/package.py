from data_structures.route import Route
import config


class Package:
    def __init__(
        self, id, address, city, state, zip, deadline, weight, status, note=""
    ):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        if not deadline == "eod".lower():
            self.deadline = Route.parse_datetime_from_string(deadline)
        else:
            self.deadline = Route.parse_datetime_from_string(config.EOD)
        self.weight = weight
        self.status = status
        self.note = note
        self.delivery_time = None

    def update_status(self, status):
        self.status = status

    def deliver(self, status=None):
        self.status = status or "Delivered"

    def __str__(self):
        return (
            f"Package ID: {self.id}\n"
            f"Address: {self.address}\n"
            f"City: {self.city}\n"
            f"State: {self.state}\n"
            f"Zip: {self.zip}\n"
            f"Deadline: {self.deadline}\n"
            f"Weight: {self.weight}\n"
            f"Note: {self.note}\n"
            f"Status: {self.status}\n"
            f"Delivery Time: {self.delivery_time}"
        )
