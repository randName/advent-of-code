directions = ((1, 0), (0, -1), (-1, 0), (0, 1))


def read_space(vm):
    scaffold = {}

    x = 0
    y = 0
    robot = None
    headings = '>^<v'

    for char in map(chr, vm):
        if char == '\n':
            x = 0
            y += 1
            continue
        if char == '#':
            scaffold[(x, y)] = True
        elif char in headings:
            robot = (x, y, headings.index(char))
        x += 1
    return scaffold, robot


def trace(scaffold, x, y, heading):
    turns = {0: None, 1: ('L', 0), -1: ('R', 0)}

    route = [0]
    done = False
    while not done:
        done = True
        for t in turns:
            nd = (heading + t) % 4
            dx, dy = directions[nd]
            np = (x + dx, y + dy)
            if scaffold.get(np):
                if t:
                    route.extend(turns[t])
                route[-1] += 1
                x, y = np
                heading = nd
                done = False
                break

    if route[0] == 0:
        route.pop(0)
    return tuple(str(i) for i in route)


def compress_route(route, max_len=20):
    routelen = len(route)
    routeset = set(range(routelen))
    routerange = range(1, routelen)

    def get_positions(segment):
        seg = len(segment)
        for i in range(routelen - seg + 1):
            if route[i:i + seg] == segment:
                yield i, tuple(range(i, i + seg))

    def get_frags(frags):
        for frag in frags:
            if not frag:
                continue
            if len(','.join(frag)) > max_len:
                break
            positions, prs = zip(*get_positions(frag))
            yield frag, positions, {p for pr in prs for p in pr}

    ends = tuple(get_frags(route[-i:] for i in routerange))

    for start, sp, ss in get_frags(route[:i] for i in routerange):
        for end, ep, es in ends:
            if ss & es:
                continue
            taken = ss | es

            sl = len(start)
            remain = (routeset - taken).union(range(sl))
            el = min(routeset - remain) + 1

            mids = (route[sl:i] for i in range(sl, el))
            for mid, mp, ms in get_frags(mids):
                if (ms & taken) or (routeset - (taken | ms)):
                    continue
                yield ((start, sp), (mid, mp), (end, ep))


def get_commands(segments):
    info = {name: seg for name, seg in zip('ABC', segments)}
    for name, seg in info.items():
        yield f'Function {name}', seg[0]

    sequence = sorted((p, n) for n, s in info.items() for p in s[1])
    yield 'Main', ''.join(name for pos, name in sequence)


if __name__ == '__main__':
    from intcode import Intcode

    with open('input/17.txt') as f:
        instructions = f.readline().strip().split(',')

    # part 1
    scaffold, robot = read_space(Intcode(instructions))

    def is_cross(x, y):
        return all(scaffold.get((x + i, y + j), 0) for i, j in directions)

    print(sum(x * y for x, y in scaffold if is_cross(x, y)))

    # part 2
    route = trace(scaffold, *robot)
    print('route:', ','.join(route))

    compressed = next(compress_route(route))

    instructions[0] = 2
    vm = Intcode(instructions)

    while True:
        line = vm.read(line=True)
        print(line)
        if not line:
            break

    commands = {
        **dict(get_commands(compressed)),
        'Continuous video feed': 'n',
    }

    while True:
        prompt = vm.read(line=True)
        if not prompt:
            print()
            break
        answer = commands.get(prompt[:-1])
        if answer is None:
            answer = input(prompt + ' ')
        else:
            answer = ','.join(answer)
        vm.sendline(answer)

    print(vm.read(line=False))
