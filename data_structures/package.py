from data_structures.route import Route
import config
import datetime


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
            self.deadline = self._parse_datetime_from_string(deadline)
        else:
            self.deadline = self._parse_datetime_from_string(config.EOD)
        self.weight = weight
        self.status = status
        self.note = note
        self.delivery_time = None
        if "delayed" in note.lower():
            self.status = "delayed"

    def is_truck_specific(self):
        return "truck" in self.note.lower()

    def is_in_group(self):
        return "delivered with" in self.note.lower()

    def has_deadline(self):
        return self.deadline != self._parse_datetime_from_string(config.EOD)

    def update_status(self, status):
        self.status = status

    def deliver(self, status=None):
        self.status = status or "Delivered"

    def is_on_truck(self):
        return "truck" in self.status.lower()

    def is_delivered(self):
        return "delivered" in self.status.lower()

    def is_delayed(self, current_time):
        if "delayed" in self.note.lower():
            delayed = current_time < self._parse_delay_time(self.note)
            if delayed:
                self.status = "delayed"
            return delayed

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

    def _parse_datetime_from_string(self, string):
        # example datetime string:
        # '1900-01-01 09:00:00'
        return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S").time()

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
