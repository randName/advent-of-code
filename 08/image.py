SIZE = (25, 6)
STRIDE = SIZE[0] * SIZE[1]

def layer(image, n):
    return image[STRIDE * n:STRIDE * (n + 1)]


if __name__ == "__main__":
    with open('input.txt') as f:
        image = tuple(int(i) for i in f.readline().strip())

    num_layers = int(len(image) / STRIDE)

    # part 1
    zeros = tuple((i, layer(image, i).count(0)) for i in range(num_layers))
    lc = layer(image, min(zeros, key=lambda x: x[1])[0])
    print(lc.count(1) * lc.count(2))

    # part 2
    output = [None for _ in range(STRIDE)]

    for i in range(STRIDE):
        for j in range(num_layers):
            p = image[j * STRIDE + i]
            if p != 2:
                output[i] = p
                break

    for i in range(SIZE[1]):
        print(output[SIZE[0] * i:SIZE[0] * (i + 1)])
