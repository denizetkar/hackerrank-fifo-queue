# Enter your code here. Read input from STDIN. Print output to STDOUT
import os


class Queue:
    def __init__(self):
        self.arr = [None]
        self.start = 0  # index to pop
        self.end = 0  # index to write the next

    def __len__(self):
        return (self.end - self.start) % len(self.arr)

    def __getitem__(self, index):
        return self.arr[(self.start + index) % len(self.arr)]

    @staticmethod
    def _gcd(a, b):
        if b == 0:
            return a
        else:
            return Queue._gcd(b, a % b)

    def _left_rotate(self, d):
        d = d % len(self.arr)
        gcd = self._gcd(d, len(self.arr))
        for i in range(gcd):
            temp = self.arr[i]
            j, k = i, (i + d) % len(self.arr)
            while k != i:
                self.arr[j] = self.arr[k]
                j, k = k, (k + d) % len(self.arr)
            self.arr[j] = temp

    def _reorder(self):
        self._left_rotate(self.start)
        length = len(self)
        self.start, self.end = 0, length

    def capacity(self):
        return len(self.arr)

    def _check_expand(self):
        remaining_cap = self.capacity() - len(self)
        if remaining_cap < 2:
            self._reorder()
            for _ in range(max(1, self.capacity() // 2)):
                self.arr.append(None)

    def enqueue(self, elem):
        self._check_expand()
        self.arr[self.end] = elem
        self.end = (self.end + 1) % len(self.arr)

    def _check_shrink(self):
        if len(self) < len(self.arr) // 2:
            self._reorder()
            for _ in range(len(self.arr) - (len(self) + 1)):
                self.arr.pop()

    def dequeue(self):
        if len(self) == 0:
            return None
        elem = self.arr[self.start]
        self.arr[self.start] = None
        self.start = (self.start + 1) % len(self.arr)
        self._check_shrink()
        return elem

    def __repr__(self) -> str:
        return "{}, {}, {}".format(repr(self.arr), self.start, self.end)


def process_queries(queries):
    q = Queue()
    for query in queries:
        query_type = query[0]
        if query_type == 1:
            q.enqueue(query[1])
        elif query_type == 2:
            q.dequeue()
        else:
            print(q[0])


if __name__ == "__main__":
    with open(os.environ["INPUT_PATH"], "r") as f:
        q = int(f.readline().strip())
        queries = []
        for _ in range(q):
            queries.append(list(map(int, f.readline().rstrip().split())))
        process_queries(queries)
