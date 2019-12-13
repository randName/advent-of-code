opcodes = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    9: 1,
}


def run(instructions):
    pointer = 0
    rel_base = 0
    mem = { i: v for i, v in enumerate(instructions) }

    def get_keys(op):
        modes = tuple(reversed('%03d' % (op // 100)))
        for i in range(opcodes.get(op % 100, 0)):
            mode = modes[i]
            p = mem[pointer + 1 + i]
            if mode == '1':
                yield None, p
            elif mode == '0':
                yield p, 0
            elif mode == '2':
                yield p + rel_base, 0

    while True:
        full_op = mem[pointer]
        op = full_op % 100

        if op == 99:
            return

        keys = tuple(get_keys(full_op))

        if op == 3:
            a = None
            while a is None:
                a = yield
            mem[keys[0][0]] = int(a)
        elif op == 4:
            yield mem.get(*keys[0])
        elif op == 9:
            rel_base += mem.get(*keys[0])
        else:
            a = mem.get(*keys[0])
            b = mem.get(*keys[1])
            c = None

            if op == 5 and a != 0:
                pointer = b
                continue

            if op == 6 and a == 0:
                pointer = b
                continue

            if op == 1:
                c = a + b
            elif op == 2:
                c = a * b
            elif op == 7:
                c = int(a < b)
            elif op == 8:
                c = int(a == b)

            if c is not None:
                mem[keys[2][0]] = c

        pointer += (opcodes.get(op, 0) + 1)


def paint(robot, hull=None):
    if hull is None:
        hull = {}

    x = 0
    y = 0
    d = 0
    try:
        next(robot)
        while True:
            col = robot.send(hull.get((x, y), 0))
            if col is None:
                continue
            hull[(x, y)] = col
            d = (d + (-1 if next(robot) else 1)) % 4
            m = 1 if d // 2 else -1
            if d % 2:
                x += m
            else:
                y += m
    except StopIteration:
        pass

    return hull


if __name__ == "__main__":
    with open('input/11.txt') as f:
        instructions = tuple(int(i) for i in f.readline().strip().split(','))

    # part 1
    print(len(paint(run(instructions))))

    # part 2
    hull = paint(run(instructions), {(0, 0): 1})

    for y in range(max(y for x, y in hull.keys()) + 1):
        for x in range(max(x for x, y in hull.keys()) + 1):
            print('.' if hull.get((x, y), 0) else ' ', end='')
        print()
