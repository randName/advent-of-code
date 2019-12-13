opcodes = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
}

def run(inst):
    pointer = 0
    done = False
    while not done:
        full_op = inst[pointer]
        op = full_op % 100

        if op == 99:
            done = True
            break

        np = opcodes[op] + 1
        modes = '%03d' % (full_op // 100)
        params = inst[pointer + 1:pointer + np]

        if op == 3:
            inst[params[0]] = int(input('enter value: '))
        elif op == 4:
            print('output: %s' % (params[0] if modes == '001' else inst[params[0]]))
        else:
            a = params[0] if modes[2] == '1' else inst[params[0]]
            b = params[1] if modes[1] == '1' else inst[params[1]]
            c = None

            if op == 5 and a != 0:
                pointer = b
                continue

            if op == 6 and a == 0:
                pointer = b
                continue

            if op == 1:
                c = a + b
            elif op == 2:
                c = a * b
            elif op == 7:
                c = int(a < b)
            elif op == 8:
                c = int(a == b)

            if c is not None:
                inst[params[2]] = c

        pointer += np


if __name__ == "__main__":
    with open('input/05.txt') as f:
        instructions = [int(i) for i in f.readline().strip().split(',')]

    run(instructions)
