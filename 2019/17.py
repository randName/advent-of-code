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

    instructions[0] = 2
    vm = Intcode(instructions)

    while True:
        line = vm.read(line=True)
        print(line)
        if not line:
            break

    commands = {
        'Main': 'ABABCBCACC',
        'Function A': ('R', '12', 'L', '10', 'L', '10'),
        'Function B': ('L',  '6', 'L', '12', 'R', '12', 'L', '4'),
        'Function C': ('L', '12', 'R', '12', 'L',  '6'),
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
