from utils import dijkstra

endpoints = {'AA', 'ZZ'}

directions = ((1, 0), (0, -1), (-1, 0), (0, 1))


class Maze:

    def __init__(self, lines):
        self.tiles = set()
        chars = {}

        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == ' ' or char == '#':
                    continue
                pos = (x, y)
                if char == '.':
                    self.tiles.add(pos)
                elif char.isalpha():
                    chars[pos] = char

        portals = {}
        labels = set()
        edgex = {0, max(x for x, y in chars) - 1}
        edgey = {0, max(y for x, y in chars) - 1}

        for pos in tuple(chars):
            if pos not in chars:
                continue
            x, y = pos
            side = 1 if (x in edgex) or (y in edgey) else -1

            for dx, dy in ((0, 1), (1, 0)):
                np = (x + dx, y + dy)
                try:
                    label = chars[pos] + chars.pop(np)
                except KeyError:
                    continue
                for tiled, jumpd in ((-1, 0), (2, 1)):
                    tp = (x + dx * tiled, y + dy * tiled)
                    if tp in self.tiles:
                        pp = (x + dx * jumpd, y + dy * jumpd)
                        break

            if label in endpoints:
                pp = tp
                side = 0
            else:
                labels.add(label)

            portals[(side, label)] = [tp, pp]

        for label in labels:
            pa, pb = (k for k, v in portals.items() if k[1] == label)
            portals[pa][0], portals[pb][0] = portals[pb][0], portals[pa][0]

        self.warp = {pos[1]: node for node, pos in portals.items()}
        self.valid = self.warp.keys() | self.tiles

        self.graph = {}
        for node, pos in portals.items():
            distances = dijkstra(pos[0], self.neighbours)
            distances.pop(pos[0])
            self.graph[node] = dict(self.portal_dists(distances, node[1]))

    def neighbours(self, current, current_dist):
        x, y = current
        newdist = current_dist + 1
        for dx, dy in directions:
            newpos = (x + dx, y + dy)
            if newpos in self.valid:
                yield newpos, newdist

    def portal_dists(self, distances, original):
        for pos in (distances.keys() & self.warp.keys()):
            side, label = self.warp[pos]
            if label == original:
                continue
            yield (-side, label), distances[pos]


if __name__ == '__main__':
    with open('input/20.txt') as f:
        maze = Maze(line for line in f if line)

    # part 1

    def neighbours_1(current, current_dist):
        for node, distance in maze.graph[current].items():
            side, label = node
            yield (-side, label), current_dist + distance

    steps = dijkstra((0, 'AA'), neighbours_1, (0, 'ZZ'))
    print(steps)

    # part 2

    def neighbours_2(current, current_dist):
        depth = current[0]
        for node, distance in maze.graph[current[1:]].items():
            side, label = node
            if depth and (side == 0):
                continue
            newdepth = depth + side
            if newdepth < 0:
                continue
            yield (newdepth, -side, label), current_dist + distance

    steps = dijkstra((0, 0, 'AA'), neighbours_2, (0, 0, 'ZZ'))
    print(steps)
