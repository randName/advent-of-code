from math import ceil
from collections import defaultdict


class Reaction:

    def __init__(self, line):
        inputs, output = line.strip().split(' => ')
        self.inputs = dict(self.parse(i) for i in inputs.split(','))
        self.output, self.count = self.parse(output)

    @staticmethod
    def parse(item):
        count, name = item.strip().split(' ')
        return name, int(count)

    def requirements(self, count=1):
        for name, n in self.inputs.items():
            yield name, n * count

    def insufficient(self, pool, count=1):
        for n, c in self.requirements(count):
            if n == 'ORE':
                continue
            if c > pool[n]:
                return True
        return False

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
        return n, max(c - self.pool[n], 0)

    def generate(self, name, count):
        if name == 'ORE' or count <= 0:
            return

        r = self.reactions.get(name)
        times = ceil(count / r.count)
        reqs = tuple(r.requirements(times))

        while r.insufficient(self.pool, times):
            for n, need in sorted(map(self.ns, reqs), key=self.ks):
                self.generate(n, need)

        self.pool[r.output] += (r.count * times)
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
