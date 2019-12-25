from itertools import combinations

directions = {'n': 'north', 's': 'south', 'e': 'east', 'w': 'west'}


class Game:

    def __init__(self, vm):
        self.vm = vm
        self.inventory = set()

    @property
    def items(self):
        return self.inventory

    @items.setter
    def items(self, value):
        ni = set(value)
        todo = {'take': ni - self.inventory, 'drop': self.inventory - ni}
        for action, stuff in todo.items():
            for item in stuff:
                self.vm.sendline(f'{action} {item}')
                self.prompt()
        self.inventory = ni

    def prompt(self):
        return self.vm.read(line=False)

    def play(self):
        while True:
            command = input(self.prompt() + ' ')
            if not command:
                break
            self.vm.sendline(command)

    def go(self, direction):
        d = directions.get(direction, direction)
        self.vm.sendline(d)

    def take(self, item):
        self.vm.sendline(f'take {item}')
        self.inventory.add(item)

    def run(self, commands):
        for command in commands:
            doors, item = self.get_room()
            if command == 't':
                self.take(item)
                continue
            self.go(command)

    def get_room(self):
        info = None
        item = None
        doors = []

        line = None
        while line != 'Command?':
            line = self.vm.read(line=True)
            if not line:
                info = None
                continue

            if line.startswith('Doors here lead:'):
                info = 'doors'
                continue
            if line.startswith('Items here:'):
                info = 'item'
                continue

            if info == 'doors':
                doors.append(line[2])
            elif info == 'item':
                item = line[2:]

        return (tuple(doors), item)


def try_items(game):
    items = tuple(game.items)
    for num in range(len(items)):
        for stuff in combinations(items, num):
            game.items = stuff
            game.go('south')
            lines = game.prompt()
            if 'heavier' in lines or 'lighter' in lines:
                continue
            return lines, stuff


if __name__ == '__main__':
    from intcode import Intcode

    with open('input/25.txt') as f:
        instructions = f.readline()

    game = Game(Intcode(instructions))
    # game.play()
    game.run('neenntstswtstnwtssstnnwtwnwts')
    print(game.items)
    prompt, answer = try_items(game)
    print('items:', ', '.join(answer))
    print(prompt)
