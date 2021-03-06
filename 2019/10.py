from math import pi, atan2, hypot
from collections import defaultdict


def get_space(f):
    for y, line in enumerate(f):
        for x, p in enumerate(line.strip()):
            if p == '#':
                yield (x, y)


def hcf(x, y):
    while y:
        x, y = y, x % y
    return x


def get_angle(station, target):
    dx = target[0] - station[0]
    dy = target[1] - station[1]
    com = hcf(dx, dy)

    x = int(dx / com)
    y = int(dy / com)

    if dx * x < 0:
        x = -x

    if dy * y < 0:
        y = -y

    return x, y


def sweep(station, angles):

    def bearing(k):
        x, y = k[0]
        return (atan2(y, x) - pi / 2 - pi) % (2 * pi)

    def distance(p):
        return hypot(station[0] - p[0], station[1] - p[1])

    for vs in angles.values():
        vs.sort(key=distance, reverse=True)

    rotation = sorted(angles.items(), key=bearing)

    for i in range(max(len(v) for v in angles.values())):
        for k, v in rotation:
            if i < len(v):
                yield v[i]


if __name__ == "__main__":
    with open('input/10.txt') as f:
        asteroids = tuple(get_space(f))

    candidates = {}
    for i in asteroids:
        angles = defaultdict(list)
        for j in asteroids:
            if j != i:
                angles[get_angle(i, j)].append(j)
        candidates[i] = angles

    # part 1
    best = max(candidates.items(), key=lambda x: len(x[1]))
    print(len(best[1]), best[0])

    # part 2
    vapour = tuple(sweep(best[0], candidates[best[0]]))
    print(vapour[199])
