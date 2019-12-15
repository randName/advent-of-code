def paint(robot, hull=None):
    if hull is None:
        hull = {}

    heading = 0
    position = [0, 0]

    while True:
        p = tuple(position)
        robot.send(hull.get(p, 0))
        try:
            hull[p], turn = tuple(robot)
        except ValueError:
            break

        heading = (heading + (-1 if turn else 1)) % 4
        direction, axis = divmod(heading, 2)
        position[axis] += (1 if direction else -1)

    return hull


if __name__ == "__main__":
    from intcode import Intcode

    with open('input/11.txt') as f:
        instructions = f.readline()

    # part 1
    print(len(paint(Intcode(instructions))))

    # part 2
    hull = paint(Intcode(instructions), {(0, 0): 1})
    for y in range(max(y for y, x in hull) + 1):
        for x in range(max(x for y, x in hull) + 1):
            print('#' if hull.get((y, x)) else ' ', end='')
        print()
