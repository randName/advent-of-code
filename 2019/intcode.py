POINTER = -1
RELATIVE_BASE = -2
ARGS = (None, 3, 3, 1, 1, 2, 2, 3, 3, 1)


class Intcode:

    def __init__(self, instructions):
        if isinstance(instructions, str):
            instructions = instructions.strip().split(',')

        self.mem = { i: int(v) for i, v in enumerate(instructions) }
        self.mem[RELATIVE_BASE] = 0
        self.mem[POINTER] = 0

        self.outputs = []
        self.machine = self.loop()
        self.send()

    @property
    def pointer(self):
        return self.mem[POINTER]

    @property
    def relative_base(self):
        return self.mem[RELATIVE_BASE]

    def send(self, value=None):
        try:
            value = int(value)
        except TypeError:
            pass

        try:
            self.machine.send(value)
        except StopIteration:
            pass

    def read(self):
        try:
            return self.outputs.pop(0)
        except IndexError:
            pass

    def __iter__(self):
        return self

    def __next__(self):
        r = self.read()
        if r is None:
            raise StopIteration
        return r

    def __getitem__(self, key):
        return self.mem.get(*key)

    def __setitem__(self, key, value):
        if value is not None:
            self.mem[key] = value

    def step(self):
        value = self.mem[self.pointer]
        self.mem[POINTER] = self.pointer + 1
        return value

    def keys(self, modes):
        for mode in map(int, reversed(modes)):
            p = self.step()
            if mode == 1:
                yield None, p
            else:
                yield p + (self.relative_base if mode else 0), 0

    def to(self, op, args):
        if op == 3:
            return args[0][0]

        if op == 9:
            return RELATIVE_BASE

        try:
            return args[2][0]
        except IndexError:
            return POINTER

    def compute(self, op, a, b=None, c=None):
        if op == 1:
            return a + b

        if op == 2:
            return a * b

        if op == 3:
            return a

        if op == 4:
            return self.outputs.append(a)

        if op == 5 and a != 0:
            return b

        if op == 6 and a == 0:
            return b

        if op == 7:
            return int(a < b)

        if op == 8:
            return int(a == b)

        if op == 9:
            return self.relative_base + a

    def loop(self):
        while True:
            modes, op = divmod(self.step(), 100)
            if op == 99:
                break

            keys = tuple(self.keys('{:0{n}}'.format(modes, n=ARGS[op])))
            values = [self[k] for k in keys]
            if op == 3:
                values[0] = yield

            self[self.to(op, keys)] = self.compute(op, *values)
