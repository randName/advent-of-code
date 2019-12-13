def parents(child, tree):
    while child:
        child = tree.get(child)
        if child:
            yield child


if __name__ == "__main__":
    with open('input/06.txt') as f:
        objs = tuple(line.strip().split(')') for line in f)

    children = { orb: cen for cen, orb in objs }

    # part 1
    total = sum(len(tuple(parents(c, children))) for c in children)
    print(total)

    # part 2
    you = tuple(parents('YOU', children))
    san = tuple(parents('SAN', children))

    for i, pair in enumerate(zip(reversed(you), reversed(san))):
        if pair[0] != pair[1]:
            break

    print(len(you) - i + len(san) - i)
