from math import gcd
from functools import reduce
from itertools import combinations


def lcm(a, b):
    return a * b // gcd(a, b)


class Dimension:

    def __init__(self, v):
        self.vel = 0
        self.pos = int(v)
        self.initial = self.pos

    @property
    def state(self):
        return self.pos, self.vel

    @property
    def home(self):
        return self.vel == 0 and self.pos == self.initial

    def step(self):
        self.pos += self.vel


class Body(dict):

    def __init__(self, pos):
        for p in pos[1:-1].split(','):
            k, v = p.strip().split('=')
            self[k] = Dimension(v)

    @property
    def kinetic(self):
        return sum(abs(v.vel) for v in self.values())

    @property
    def potential(self):
        return sum(abs(v.pos) for v in self.values())

    @property
    def energy(self):
        return self.kinetic * self.potential

    @property
    def state(self):
        return tuple(zip(*(d.state for d in self.values())))

    def __repr__(self):
        return 'Body %s %s' % self.state

    def step(self):
        for d in self.values():
            d.step()


class Sim:

    def __init__(self, bodies):
        self.bodies = tuple(bodies)
        self.accel = ((-1, 1), (1, -1))
        self.periods = {k: None for k in 'xyz'}

    def __str__(self):
        return ' '.join(str(b) for b in self.bodies)

    def energies(self):
        for b in self.bodies:
            yield b.energy

    def step(self):
        for a, b in combinations(self.bodies, 2):
            for d in 'xyz':
                pa = a[d].pos
                pb = b[d].pos
                if pa == pb:
                    continue

                aa, ab = self.accel[int(pa < pb)]
                a[d].vel += aa
                b[d].vel += ab

        for b in self.bodies:
            b.step()

    def check(self, s):
        for d in 'xyz':
            if self.periods[d] is not None:
                continue
            if all(b[d].home for b in self.bodies):
                self.periods[d] = s

        return all(self.periods.values())


if __name__ == "__main__":
    with open('input/12.txt') as f:
        moons = Sim(Body(line.strip()) for line in f)

    for i in range(1000):
        moons.step()
        moons.check(i + 1)

    # part 1
    print(sum(moons.energies()))

    while True:
        i += 1
        if moons.check(i):
            break
        moons.step()

    # part 2
    print(reduce(lcm, moons.periods.values()))
