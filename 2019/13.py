class Game:

    def __init__(self, vm):
        self.vm = vm
        self.grid = {}
        self.running = True
        self.refresh()

    def refresh(self):
        updates = tuple(self.vm)
        if not updates:
            self.running = False
            return

        for i in range(len(updates) // 3):
            x, y, t = updates[i * 3:i * 3 + 3]
            if x == -1 and y == 0:
                self.display = t
            else:
                self.grid[x, y] = t

                if t == 3:
                    self.paddle = x
                elif t == 4:
                    self.ball = x

    def joy(self, direction):
        self.vm.send(direction)
        self.refresh()


if __name__ == '__main__':
    from intcode import Intcode

    with open('input/13.txt') as f:
        instructions = f.readline().strip().split(',')

    # part 1
    game = Game(Intcode(instructions))
    print(len(tuple(p for p in game.grid.values() if p == 2)))

    # part 2
    instructions[0] = 2

    game = Game(Intcode(instructions))
    while game.running:
        m = game.ball - game.paddle
        game.joy(0 if not m else (m / abs(m)))

    print(game.display)
