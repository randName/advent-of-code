def base(n):
    for i in range(n):
        yield (0, 1, 0, -1)


def pattern(i):
    first, *seq = tuple(j for i in zip(*base(i + 1)) for j in i)
    seq.append(first)
    while True:
        yield from seq


def phase(signal):
    for i in range(len(signal)):
        yield abs(sum((a * b) for a, b in zip(signal, pattern(i)))) % 10


def reversed_cumsums(values):
    total = sum(values)
    for v in values:
        yield total % 10
        total -= v


if __name__ == '__main__':
    with open('input/16.txt') as f:
        signal = tuple(int(i) for i in f.readline().strip())

    # part 1
    sig = signal
    for i in range(100):
        sig = tuple(phase(sig))
    print(sig[:8])

    # part 2
    offset = int(''.join(str(s) for s in signal[:7]))
    actual = (signal * 10000)[offset:]

    for i in range(100):
        actual = tuple(reversed_cumsums(actual))
    print(actual[:8])
