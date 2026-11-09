import numpy as np


class MyHashMap:
    MAX_LOAD_FACTOR = 0.75

    def __init__(self, capacity=8):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]

    def _index(self, key):
        return hash(key) % self.capacity

    def load_factor(self):
        return self.size / self.capacity

    def _resize(self):
        old_buckets = self.buckets

        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]

        self.size = 0

        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)

    def put(self, key, value):
        idx = self._index(key)
        bucket = self.buckets[idx]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        if (self.size + 1) / self.capacity > self.MAX_LOAD_FACTOR:
            self._resize()
            idx = self._index(key)
            bucket = self.buckets[idx]

        bucket.append((key, value))
        self.size += 1

    def get(self, key):
        idx = self._index(key)
        bucket = self.buckets[idx]

        for k, v in bucket:
            if k == key:
                return v

        return None

    def contains(self, key):
        return self.get(key) is not None

    def remove(self, key):
        idx = self._index(key)
        bucket = self.buckets[idx]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return True

        return False

    def __len__(self):
        return self.size


class SegmentTree:

    def __init__(self, a):
        self.length = len(a)
        if self.length == 0:
          raise ValueError('Пустой массив не поддерживается')

        self.a = list(a) # копия исходного массива
        self.tree = [0] * (4 * self.length)
        self._build(1, 0, self.length - 1)

    def _build(self, v, tl, tr):
        if tl == tr:
          self.tree[v] = self.a[tl]
          return

        tm = (tl + tr) // 2

        self._build(2 * v, tl, tm)
        self._build(2 * v + 1, tm + 1, tr)

        self.tree[v] = self.tree[2 * v] + self.tree[2 * v + 1]

    def query(self, l, r):
        if l < 0 or r >= self.length or l > r:
            raise IndexError("Некорректные границы запроса")
        return self._query(1, 0, self.length - 1, l, r)

    def _query(self, v, tl, tr, l, r):
        if r < tl or tr < l:
            return 0

        if l <= tl and tr <= r:
            return self.tree[v]

        tm = (tl + tr) // 2
        left_sum = self._query(2 * v, tl, tm, l, r)
        right_sum = self._query(2 * v + 1, tm + 1, tr, l, r)
        return left_sum + right_sum

    def update(self, pos, value):
        if pos < 0 or pos >= self.length:
            raise IndexError("Некорректная позиция обновления")

        self.a[pos] = value
        self._update(1, 0, self.length - 1, pos, value)

    def _update(self, v, tl, tr, pos, value):
        if tl == tr:
            self.tree[v] = value
            return

        tm = (tl + tr) // 2

        if pos <= tm:
            self._update(2 * v, tl, tm, pos, value)
        else:
            self._update(2 * v + 1, tm + 1, tr, pos, value)

        self.tree[v] = self.tree[2 * v] + self.tree[2 * v + 1]


class BinarySearch:

    def __init__(self, data):
        self.data = np.array(data)

    def _check(self, x, k):
        return np.sum(self.data <= x) >= k

    def find_threshold(self, k):
        if len(self.data) < k:
            return None

        left = int(np.floor(self.data.min()))
        right = int(np.ceil(self.data.max()))

        while left < right:
            mid = (left + right) // 2
            if self._check(mid, k):
                right = mid
            else:
                left = mid + 1

        return left


class BinaryHeap:

    def __init__(self):
        self.heap = []

    def insert(self, flight_id, delay):

        self.heap.append((delay, flight_id))
        self._sift_up(len(self.heap) - 1)

    def _sift_up(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.heap[index][0] > self.heap[parent][0]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._sift_up(parent)

    def extract_max(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        max_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return max_val

    def _sift_down(self, index):
        largest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < len(self.heap) and self.heap[left][0] > self.heap[largest][0]:
            largest = left
        if right < len(self.heap) and self.heap[right][0] > self.heap[largest][0]:
            largest = right

        if largest != index:
            self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
            self._sift_down(largest)


def calculate_pagerank(routes, num_iterations=20, d=0.85):
    airports = set()
    for origin, dest in routes:
        airports.add(origin)
        airports.add(dest)

    n = len(airports)
    if n == 0: return {}

    ranks = {airport: 1.0 / n for airport in airports}

    out_links = {airport: [] for airport in airports}
    for origin, dest in routes:
        out_links[origin].append(dest)

    for _ in range(num_iterations):
        new_ranks = {}
        for airport in airports:
            rank = (1 - d) / n

            for other in airports:
                if airport in out_links[other]:
                    rank += d * (ranks[other] / len(out_links[other]))

            new_ranks[airport] = rank
        ranks = new_ranks

    return sorted(ranks.items(), key=lambda x: x[1], reverse=True)