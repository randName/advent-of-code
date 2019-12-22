def modinv(n, p):
    # only for prime p
    return pow(n, p - 2, p)


def parse_shuffle(lines):
    for line in lines:
        line = line.strip().split(' ')
        try:
            yield line[0], int(line[-1])
        except ValueError:
            yield 'flip', 0


def technique(name, n, i):
    if name == 'flip':
        return (-1 - i)

    if name == 'deal':
        return i * n

    if name == 'cut':
        return i - n


if __name__ == '__main__':
    with open('input/22.txt') as f:
        shuffle = tuple(parse_shuffle(f))

    # part 1
    card = 2019
    deck = 10007
    for name, n in shuffle:
        card = technique(name, n, card) % deck
    print(card)

    # part 2
    card = 2020
    deck = 119315717514047
    reps = 101741582076661

    def reverse_shuffle(card):
        for name, n in reversed(shuffle):
            if name == 'deal':
                n = -modinv(n, deck)
            card = technique(name, -n, card) % deck
        return card

    b = reverse_shuffle(0)
    a = (reverse_shuffle(1) - b) % deck

    raised = pow(a, reps, deck)
    series = (raised - 1) * modinv(a - 1, deck)
    print((card * raised + b * series) % deck)
