from data_structures.package import Package


class HashTable:
    def __init__(self, file_path=None, size=100):
        self.size = size
        self.table = [[] for _ in range(self.size)]
        if file_path:
            self.load_package_data(file_path)

    def _hash(self, key):
        return key % self.size

    def insert(self, key, val):
        hash_index = self._hash(key)
        for item in self.table[hash_index]:
            if item[0] == key:
                item[1] = val
                return
        self.table[hash_index].append([key, val])

    def lookup(self, key):
        hash_index = self._hash(key)
        for item in self.table[hash_index]:
            if item[0] == key:
                return item[1]
        return None  # Key not found

    def remove(self, key):
        hash_index = self._hash(key)
        for i, item in enumerate(self.table[hash_index]):
            if item[0] == key:
                del self.table[hash_index][i]
                return
        raise KeyError(key)  # Key not found

    def get_all_ids(self):
        ids = []
        for bucket in self.table:
            for item in bucket:
                ids.append(item[0])
        return ids

    def __str__(self):
        return str(self.table)

    def __iter__(self):
        for bucket in self.table:
            for _, value in bucket:
                yield value

    def __len__(self):
        return sum(len(bucket) for bucket in self.table)

    def load_package_data(self, file_path):
        # open the file in read mode
        with open(file_path, "r") as file:
            # read the lines from the file, skipping the first line (header)
            lines = file.readlines()[1:]
            # create an empty list to store the packages
            packages = []
            # iterate through the lines
            for line in lines:
                # split the line by the comma
                data = line.strip().split(",")
                # extract the package data
                package_id = int(data[0])
                address = data[1]
                city = data[2]
                state = data[3]
                zip_code = data[4]
                deadline = data[5]
                weight = data[6]
                note = data[7]
                status = "At Hub"  # initialize status to "At Hub"

                package = Package(
                    package_id,
                    address,
                    city,
                    state,
                    zip_code,
                    deadline,
                    weight,
                    status,
                    note,
                )
                # add the package to the list
                packages.append(package)
            # return the list of packages

            for package in packages:
                self.insert(package.id, package)
