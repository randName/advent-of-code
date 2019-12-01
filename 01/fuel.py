def compute_fuel(mass):
    return mass // 3 - 2


def compute_fuel_2(mass):
    f = compute_fuel(mass)
    total = 0

    while f > 0:
        total += f
        f = compute_fuel(f)

    return total


if __name__ == "__main__":
    with open('input.txt') as f:
        modules = tuple(int(line.strip()) for line in f)

    # part 1
    print(sum(compute_fuel(m) for m in modules))

    # part 2
    print(sum(compute_fuel_2(m) for m in modules))
