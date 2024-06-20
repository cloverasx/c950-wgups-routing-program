class DistanceCalculator:
    def __init__(self, distances):
        self.distances = distances

    def get_distance(self, address1, address2):
        return self.distances[address1][address2]