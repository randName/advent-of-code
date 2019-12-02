def run(inst):
    pointer = 0
    done = False
    while not done:
        op = inst[pointer]

        if op == 99:
            done = True
        else:
            a = inst[pointer + 1]
            b = inst[pointer + 2]
            c = inst[pointer + 3]

            if op == 1:
                inst[c] = inst[a] + inst[b]
            elif op == 2:
                inst[c] = inst[a] * inst[b]

            pointer += 4


if __name__ == "__main__":
    with open('input.txt') as f:
        instructions = tuple(int(i) for i in f.readline().strip().split(','))

    # part 1
    inst = list(instructions)
    inst[1] = 12
    inst[2] = 2
    run(inst)
    print(inst[0])

    # part 2
    for i in range(100):
        for j in range(100):
            inst = list(instructions)
            inst[1] = i
            inst[2] = j

            run(inst)

            if inst[0] == 19690720:
                print('%02d%02d' % (i, j))
                break
