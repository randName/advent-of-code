directions = ((1, 0), (0, -1), (-1, 0), (0, 1))


class Bugs:

    def __init__(self, grid=None, size=5, level=None):
        self.size = size
        self.level = level or {}

        if grid is None:
            grid = {}

        self.all = set()
        self.alive = set()

        for y in range(size):
            for x in range(size):
                pos = (x, y)
                if level and pos == (2, 2):
                    continue
                self.all.add(pos)
                if grid.get(pos):
                    self.alive.add(pos)

        self.fresh = True

    @property
    def population(self):
        return len(self.alive)

    @property
    def child(self):
        return self.level.get(1)

    @property
    def parent(self):
        return self.level.get(-1)

    def edge(self, dx, dy):
        size = self.size
        if not dx:
            y = 2 - 2 * dy
            return ((1, x, y) for x in range(size))
        else:
            x = 2 - 2 * dx
            return ((1, x, y) for y in range(size))

    def hood(self, pos):
        x, y = pos
        for dx, dy in directions:
            np = (x + dx, y + dy)
            if np in self.all:
                yield (0, *np)
            elif self.level:
                if np == (2, 2):
                    yield from self.edge(dx, dy)
                else:
                    yield (-1, 2 + dx, 2 + dy)

    def get_alive(self, dl):
        level = self.level.get(dl)
        if level is None:
            nl = self.level[0] + dl
            self.level[dl] = Bugs(level={0: nl, -dl: self, dl: None})
            return set()
        return {(dl, *p) for p in level.alive}

    def compute_delta(self):
        alive = {(0, *p) for p in self.alive}
        if self.level:
            for dl in (-1, 1):
                if self.fresh and (dl * self.level[0]) > 0:
                    continue
                alive |= self.get_alive(dl)

        self.births = set()
        self.deaths = set()

        for pos in self.all:
            count = sum(1 for p in self.hood(pos) if p in alive)
            if pos in self.alive:
                if count != 1:
                    self.deaths.add(pos)
            else:
                if count in {1, 2}:
                    self.births.add(pos)

        if self.level:
            level = self.level[0]

            if self.parent and level <= 0:
                self.parent.compute_delta()

            if self.child and level >= 0:
                self.child.compute_delta()

    def step(self):
        level = self.level.get(0)
        if not level:
            self.compute_delta()

        self.alive -= self.deaths
        self.alive |= self.births
        self.fresh = False

        if self.level is not None:
            if self.parent and level <= 0:
                self.parent.step()

            if self.child and level >= 0:
                self.child.step()


def parse_cells(lines):
    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            yield (x, y), (char == '#')


def find_repeat(ca):
    history = set([frozenset(ca.alive)])
    while True:
        ca.step()
        cur = frozenset(ca.alive)
        if cur in history:
            return cur
        history.add(cur)


def dig(ca, direction, depth=None):
    d = 0
    while ca:
        ca = ca.level.get(direction)
        if ca:
            yield ca
        d += 1
        if depth and d >= depth:
            break


if __name__ == '__main__':
    with open('input/24.txt') as f:
        scan = dict(parse_cells(f))

    # part 1
    ca = Bugs(scan)
    repeat = find_repeat(ca)
    print(sum((1 << (y * 5 + x)) for x, y in repeat))

    # part 2
    ca = Bugs(scan, level={0: 0})
    for i in range(200):
        ca.step()

    total = sum(lv.population for lv in (*dig(ca, -1), ca, *dig(ca, 1)))
    print(total)
