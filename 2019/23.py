class Machine:

    def __init__(self, address, vm):
        self.vm = vm
        self.buf = []
        self.waiting = None

        self.vm.send(address)

    @property
    def idle(self):
        return self.waiting and (not self.buf)

    def io(self):
        dest = self.vm.read()

        if dest is not None:
            self.waiting = False
            x = self.vm.read()
            y = self.vm.read()
            return dest, (x, y)

        self.waiting = True
        try:
            x, y = self.buf.pop(0)
            self.vm.send(x)
            self.vm.send(y)
        except IndexError:
            self.vm.send(-1)

        return None, None

    def send(self, packet):
        self.buf.append(packet)


if __name__ == '__main__':
    from intcode import Intcode

    with open('input/23.txt') as f:
        instructions = f.readline()

    part_1 = True
    network = tuple(Machine(i, Intcode(instructions)) for i in range(50))

    nat_packet = None
    resume_hist = set()

    while True:
        for m in network:
            dest, packet = m.io()
            if dest == 255:
                if part_1:
                    print(packet[1])
                    part_1 = False
                nat_packet = packet
            elif packet:
                network[dest].send(packet)

        # part 2
        if nat_packet and all(m.idle for m in network):
            network[0].send(nat_packet)
            y = nat_packet[1]
            if y in resume_hist:
                print(y)
                break
            else:
                resume_hist.add(y)
            nat_packet = None
