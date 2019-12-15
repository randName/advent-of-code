from math import ceil
from collections import defaultdict


class Reaction:

    def __init__(self, line):
        inputs, output = line.strip().split(' => ')
        self.inputs = dict(self.parse(i) for i in inputs.split(','))
        self.names = tuple(sorted(self.inputs, key=self.key))
        self.output, self.count = self.parse(output)

    @staticmethod
    def parse(item):
        count, name = item.strip().split(' ')
        return name, int(count)

    def key(self, name):
        return 0 if name == 'ORE' else -self.inputs[name]

    def __getitem__(self, count):
        times = ceil(count / self.count)
        for name in self.names:
            yield name, self.inputs[name] * times
        yield self.output, -self.count * times

    def __repr__(self):
        return '<Reaction (%d %s)>' % (self.count, self.output)


class Factory:

    def __init__(self, lines):
        self.reactions = {}
        for line in lines:
            r = Reaction(line)
            self.reactions[r.output] = r

        self.pool = defaultdict(int)

    @property
    def ores(self):
        return -self.pool['ORE']

    @staticmethod
    def ks(k):
        return -k[1]

    def reset(self):
        self.pool.clear()

    def ns(self, k):
        n, c = k
        return n, c - self.pool[n]

    def insufficient(self, chemicals):
        for n, c in chemicals:
            if n == 'ORE' or c <= 0:
                continue
            if self.pool[n] < c:
                return True
        return False

    def generate(self, name, count):
        if name == 'ORE' or count <= 0:
            return

        reqs = tuple(self.reactions.get(name)[count])

        while self.insufficient(reqs):
            for n, need in sorted(map(self.ns, reqs), key=self.ks):
                self.generate(n, need)

        for n, c in reqs:
            self.pool[n] -= c


if __name__ == '__main__':
    with open('input/14.txt') as f:
        factory = Factory(f)

    # part 1
    factory.generate('FUEL', 1)
    print(factory.ores)

    # part 2
    limit = 1000000000000
    guess = 1000000
    diff = 1

    while diff > 0:
        factory.reset()
        factory.generate('FUEL', int(guess))
        diff = limit - factory.ores
        guess *= (1 + diff / limit)

    print(int(guess))
