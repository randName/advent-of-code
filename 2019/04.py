def check(number):
    s = str(number)

    double = sum(a == b for a, b in zip(s[:-1], s[1:]))

    if double < 1:
        return False

    if any(int(b) < int(a) for a, b in zip(s[:-1], s[1:])):
        return False

    return True


def check2(number):
    if not check(number):
        return False

    cur = None
    n = 0
    counts = []

    for c in str(number):
        if c != cur:
            counts.append((cur, n))
            n = 0

        cur = c
        n += 1

    counts.append((cur, n))

    if sum(n == 2 for c, n in counts) < 1:
        return False

    return True


if __name__ == "__main__":
    # part 1
    print(check(111111))
    print(check(223450))
    print(check(123789))

    print(sum(check(i) for i in range(206938, 679129)))

    # part 2
    print(check2(112233))
    print(check2(123444))
    print(check2(111122))

    print(sum(check2(i) for i in range(206938, 679129)))
