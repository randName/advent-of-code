if __name__ == "__main__":
    from intcode import Intcode

    with open('input/09.txt') as f:
        instructions = f.readline()

    # part 1
    vm = Intcode(instructions)
    vm.send(1)
    print(vm.read())

    # part 2
    vm = Intcode(instructions)
    vm.send(2)
    print(vm.read())
