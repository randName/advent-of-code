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


if __name__ == "__main__":
    with open('input.txt') as f:
        instructions = tuple(int(i) for i in f.readline().strip().split(','))

    # part 1
    o = run(instructions)
    next(o)
    print(o.send(1))

    # part 2
    o = run(instructions)
    next(o)
    print(o.send(2))
