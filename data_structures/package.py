class Package:
    def __init__(
        self, id, address, city, state, zip, deadline, weight, status, note=""
    ):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.note = note

    def update_status(self, status):
        self.status = status

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
            f"Status: {self.status}"
        )
