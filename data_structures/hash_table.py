class HashTable:
    def __init__(self):
        self.MAX = 100
        self.arr = [None for i in range(self.MAX)]

    def _hash(self, key):
        h = 0
        for char in key:
            h += ord(char)
        return h % self.MAX

    def insert(self, key, val):
        h = self._hash(key)
        self.arr[h] = val

    def lookup(self, key):
        h = self._hash(key)
        return self.arr[h]

    def remove(self, key):
        h = self._hash(key)
        self.arr[h] = None