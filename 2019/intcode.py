class Intcode:

    opcodes = (None, 3, 3, 1, 1, 2, 2, 3, 3, 1)

    operator = {
        1: lambda a, b: a + b,
        2: lambda a, b: a * b,
        7: lambda a, b: int(a < b),
        8: lambda a, b: int(a == b),
    }

    def __init__(self, instructions):
        if isinstance(instructions, str):
            instructions = instructions.strip().split(',')

        self.mem = { i: int(v) for i, v in enumerate(instructions) }

        self.pointer = 0
        self.rel_base = 0

        self.outputs = []
        self.machine = self.loop()
        self.send(None)

    def send(self, value):
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
        self.mem[key[0]] = value

    def parse(self):
        op = self.mem[self.pointer]
        modes = tuple(reversed('%03d' % (op // 100)))
        op %= 100
        yield op
        if op == 99:
            return

        for i in range(self.opcodes[op]):
            mode = modes[i]
            p = self.mem[self.pointer + 1 + i]
            if mode == '1':
                yield None, p
            else:
                yield p + (0 if mode == '0' else self.rel_base), 0

    def loop(self):
        while True:
            op, *keys = self.parse()
            if op == 99:
                break

            if op == 3:
                a = yield
                self[keys[0]] = int(a)
            elif op == 4:
                self.outputs.append(self[keys[0]])
            elif op == 9:
                self.rel_base += self[keys[0]]
            else:
                a = self[keys[0]]
                b = self[keys[1]]

                if (op == 5 and a != 0) or (op == 6 and a == 0):
                    self.pointer = b
                    continue

                try:
                    self[keys[2]] = self.operator[op](a, b)
                except KeyError:
                    pass

            self.pointer += (self.opcodes[op] + 1)
