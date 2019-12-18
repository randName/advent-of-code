POINTER = -1
OUTPUTS = -2
RELATIVE_BASE = -3


class Intcode:

    nargs = (None, 3, 3, 1, 1, 2, 2, 3, 3, 1)

    def __init__(self, ints='99', **kw):
        self.mem = dict(kw.get('state', self.from_ints(ints)))
        self.machine = self.cycle()
        self.send()

    @property
    def pointer(self):
        return self.mem[POINTER]

    @property
    def outputs(self):
        return self.mem[OUTPUTS]

    @property
    def relative_base(self):
        return self.mem[RELATIVE_BASE]

    def send(self, value=None):
        try:
            self.machine.send(value)
        except StopIteration:
            pass

    def sendline(self, line):
        for char in line:
            self.send(ord(char))
        self.send(10)

    def read(self, line=None):
        if line is not None:
            return ''.join(self.readline(line)).strip()
        try:
            return self.outputs.pop(0)
        except IndexError:
            pass

    def readline(self, line):
        for char in self:
            yield str(char) if char > 255 else chr(char)
            if line and char == 10:
                break

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
        if value is None:
            return
        self.mem[key] = value

    def address(self, mode):
        value = self.fetch()
        if mode == 1:
            return None, value
        return value + (self.relative_base if mode else 0), 0

    def fetch(self):
        value = self.mem[self.pointer]
        self.mem[POINTER] = self.pointer + 1
        return value

    def decode(self):
        modes, op = divmod(self.fetch(), 100)
        return op, tuple(map(int, reversed(f'{modes:0{self.nargs[op]}}')))

    def execute(self, op, a, b=None, c=None):
        if op == 1:
            return a + b

        if op == 2:
            return a * b

        if op == 3:
            return int(a)

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

    def cycle(self):
        while True:
            self.current = self.pointer
            try:
                op, modes = self.decode()
            except IndexError:
                break

            addresses = tuple(map(self.address, modes))
            values = [self[a] for a in addresses]
            if op == 3:
                values[0] = yield

            if op == 9:
                destination = RELATIVE_BASE
            elif op == 5 or op == 6:
                destination = POINTER
            else:
                destination = addresses[-1][0]

            self[destination] = self.execute(op, *values)
        self.current = None

    def clone_state(self):
        for k, v in self.mem.items():
            if k == OUTPUTS:
                v = v[:]
            elif k == POINTER:
                v = self.current or 0
            yield k, v

    def clone(self, **kw):
        return Intcode(state=self.clone_state(), **kw)

    @staticmethod
    def from_ints(ints):
        if isinstance(ints, str):
            ints = ints.strip().split(',')

        yield POINTER, 0
        yield OUTPUTS, []
        yield RELATIVE_BASE, 0

        for i, v in enumerate(ints):
            yield i, int(v)
