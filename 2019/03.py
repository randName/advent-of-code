directions = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
}


def trace(line):
    x = 0
    y = 0
    s = 0
    route = {}

    for i in line.split(','):
        dx, dy = directions[i[0]]
        for j in range(int(i[1:])):
            x += dx
            y += dy
            s += 1
            route[(x, y)] = s

    return route


if __name__ == "__main__":
    with open('input/03.txt') as f:
        wires = tuple(line.strip() for line in f)

    # part 1
    a, b = map(trace, wires)
    intersections = a.keys() & b.keys()
    print(min(abs(x) + abs(y) for x, y in intersections))

    # part 2
    print(min(a[k] + b[k] for k in intersections))
