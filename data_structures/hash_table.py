class HashTable:
    # def __init__(self):
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(self.size)]

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

    def __str__(self):
        return str(self.table)
