class Package:
    def __init__(self, id, address, city, state, zip, deadline, weight, status):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.status = status

    def update_status(self, status):
        self.status = status

    def __str__(self):
        return f"Package ID: {self.id}\nAddress: {self.address}\nCity: {self.city}\nState: {self.state}\nZip: {self.zip}\nDeadline: {self.deadline}\nWeight: {self.weight}\nStatus: {self.status}"