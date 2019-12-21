def get_script(end):
    while True:
        instr = input('> ').strip()
        if instr:
            yield instr
        else:
            break


if __name__ == '__main__':
    from intcode import Intcode

    with open('input/21.txt') as f:
        instructions = f.readline()

    def run_script(script, end):
        vm = Intcode(instructions)
        vm.read(line=False)
        for line in script:
            vm.sendline(line)
        vm.sendline(end)
        print(vm.read(line=False))

    # part 1
    # not (((not D) or C) and A)
    part_1 = ('NOT D J', 'OR C J', 'AND A J', 'NOT J J')
    run_script(part_1, 'WALK')

    # part 2
    # not ((not ((E or H) and (not C) and D)) and (B or E) and A)
    part_2 = (
        'OR H J', 'OR E J', 'NOT C T', 'AND D J', 'AND T J', 'NOT J J',
        'OR B T', 'OR E T', 'AND T J', 'AND A J', 'NOT J J',
    )
    run_script(part_2, 'RUN')
