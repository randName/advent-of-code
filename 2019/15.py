from collections import defaultdict

class Robot:

    def __init__(self, vm):
        self.vm = vm
        self.target = None
        self.position = (0, 0)
        self.walls = {self.position: False}

    def step(self, direction):
        pos = list(self.position)
        axis, d = divmod(direction, 2)
        pos[1 - axis] += (1 if d else -1)
        return tuple(pos)

    def move(self, direction):
        self.vm.send(direction + 1)
        return self.vm.read()

    def poke(self, direction):
        newpos = self.step(direction)
        wall = self.walls.get(newpos)
        if wall is not None:
            return not wall

        status = self.move(direction)

        if not status:
            self.walls[newpos] = True
            return False

        if status == 2:
            self.target = newpos

        self.walls[newpos] = False
        self.move((1, 0, 3, 2)[direction])
        return True

    def explore(self):
        for i in range(4):
            if self.poke(i):
                yield self.step(i), i

    def show(self):
        xs = tuple(x for x, y in self.walls)
        ys = tuple(y for x, y in self.walls)
        for y in range(min(ys), max(ys) + 1):
            for x in range(min(xs), max(xs) + 1):
                w = self.walls.get((x, y))
                p = ' '
                if w is None:
                    p = '?'
                elif w:
                    p = '#'
                print(p, end='')
            print()


if __name__ == '__main__':
    from intcode import Intcode

    with open('input/15.txt') as f:
        instructions = f.readline()

    went = defaultdict(int)
    robot = Robot(Intcode(instructions))

    def step():
        went[robot.position] += 1
        robot.position, d = min(robot.explore(), key=lambda x: went[x[0]])
        robot.move(d)

    # part 1
    route = [None, (0, 0)]
    while not robot.target:
        step()
        if robot.position == route[-2]:
            route.pop()
            continue
        route.append(robot.position)
    print(len(route) - 2)

    # part 2
    for i in range(100):
        step()
    robot.show()

    done = False
    oxygen = {robot.target: 0}
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
    while not done:
        done = True
        for pos in tuple(oxygen):
            if oxygen[pos] == 0:
                for dx, dy in directions:
                    p = (pos[0] + dx, pos[1] + dy)
                    if robot.walls.get(p) or p in oxygen:
                        continue
                    oxygen[p] = 0
                    done = False
            oxygen[pos] += 1
    print(max(oxygen.values()) - 1)
