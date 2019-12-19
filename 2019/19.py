from math import atan2, tan


def midway(beamset):
    mx = max(x for x, y in beamset)
    my = max(y for x, y in beamset)
    ay = atan2(my, min(x for x, y in beamset if y == my))
    ax = atan2(min(y for x, y in beamset if x == mx), mx)
    return tan((ax + ay) / 2)


def get_left(y, angle):
    x = int(y / angle)
    for left in range(x, 0, -1):
        if not beam(left - 1, y):
            return left


if __name__ == '__main__':
    from intcode import Intcode
    with open('input/19.txt') as f:
        instructions = f.readline().strip().split(',')

    beam_cache = {}

    def beam(x, y):
        try:
            return beam_cache[(x, y)]
        except KeyError:
            pass

        vm = Intcode(instructions)
        vm.send(x)
        vm.send(y)
        return beam_cache.setdefault((x, y), vm.read())

    # part 1
    affected = sum(beam(x, y) for x in range(50) for y in range(50))
    print(affected)

    # part 2
    angle = midway(set(p for p, b in beam_cache.items() if b))
    target = 100 - 1

    lower = 0
    upper = 2000
    guessing = True

    while True:
        if guessing:
            y = (lower + upper) // 2
        else:
            y += 1

        x = get_left(y, angle)

        if not guessing:
            top = y - target
            if beam(x + target, top):
                y = top
                break

        for size in range(2, y):
            c = size - 1
            if not beam(x + c, y - c):
                break

        if size > target:
            upper = y
        elif size < target:
            lower = y
        else:
            guessing = False

    print(x * 10000 + y)
