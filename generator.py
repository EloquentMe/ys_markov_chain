import random
import json


class storage:

    def __init__(self):
        self.single = {}
        self.double = {}

    def getrandom(words, total):
        n = random.randint(1, total)
        for word, prob in words:
            if n < prob:
                break
            n = n - prob
        return word
    getrandom = staticmethod(getrandom)

    def load(self, filename):
        storage = {}
        with open(filename, 'r') as f:
            storage = json.load(f)
        self.single = storage['single']
        self.double = storage['double']

    def dump(self, filename):
        storage = {}
        storage['single'] = self.single
        storage['double'] = self.double
        with open(filename, 'w') as f:
            json.dump(storage, f)

    def add_two(self, previous, current):
        p1, p2 = previous
        wordstore1 = self.double.setdefault(p1, {})
        wordstore2 = wordstore1.setdefault(p2, {})
        wordcount = wordstore2.setdefault(current, 0)
        wordcount += 1
        wordstore2[current] = wordcount

    def add_one(self, previous, current):
        wordstore = self.single.setdefault(previous, {})
        count = wordstore.setdefault(current, 0)
        count += 1
        wordstore[current] = count

    def get_two(self, previous, current):
        words = self.double[previous][current]
        total = sum(words.values())
        return storage.getrandom(words.items(), total)

    def get_one(self, previous):
        words = self.single[previous]
        total = sum(words.values())
        return storage.getrandom(words.items(), total)


def is_terminator(line):
    if line in {'.', '?', '!'}:
        return True
    else:
        return False


def collect(stream, filename):
    prev = curr = nextword = None
    store = storage()
    for line in stream:
        prev, curr = curr, nextword
        nextword = line.strip()
        if prev == None and curr != None:
            store.add_one(curr, nextword)
        elif prev != None and curr != None:
            store.add_two((prev, curr), nextword)

        if is_terminator(nextword):
            nextword = '.'
            curr = None
        if is_terminator(curr):
            curr = None
    store.dump(filename)


def generate(stream, filename, total=10000):
    store = storage()
    store.load(filename)
    prev = curr = nextword = None
    for amount in range(total):
        prev, curr = curr, nextword
        if prev == None and curr == None:
            nextword = store.get_one('.')
        elif prev == None and curr != None:
            nextword = store.get_one(curr)
        else:
            nextword = store.get_two(prev, curr)

        if is_terminator(nextword):
            stream.write(nextword)
            if random.choice([True, False]):
                stream.write('\n')
            prev = curr = nextword = None
        else:
            stream.write(' ' + nextword)
