from utils import dijkstra

directions = ((1, 0), (0, -1), (-1, 0), (0, 1))


class Maze:

    def __init__(self, lines):
        self.items = {}
        self.keys = set()
        self.doors = set()
        self.walls = set()

        start = set()
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                pos = (x, y)
                if char == '#':
                    self.walls.add(pos)
                elif char == '.':
                    pass
                elif char == '@':
                    start.add(pos)
                else:
                    self.items[pos] = char.lower()
                    if char.isupper():
                        self.doors.add(pos)
                    else:
                        self.keys.add(pos)

        self.numkeys = len(self.keys)
        self.start = {i: v for i, v in enumerate(start)}

    def compute_graph(self):
        self.graph = {i: dict(self.key_dist(p)) for i, p in self.start.items()}
        for key in self.keys:
            self.graph[self.items[key]] = dict(self.key_dist(key))

    def neighbours(self, node, current_dist):
        x, y = node
        newdist = current_dist + 1
        for dx, dy in directions:
            newpos = (x + dx, y + dy)
            if newpos in self.walls:
                continue
            yield newpos, newdist

    def key_dist(self, position):
        distances, paths = dijkstra(position, self.neighbours, paths=True)
        for key in (distances.keys() & self.keys):
            if key == position:
                continue
            doors = self.doors.intersection(paths[key])
            info = (distances[key], {self.items[d] for d in doors})
            yield self.items[key], info


def update_for_part_2(maze):
    i = 0
    sx, sy = maze.start.pop(0)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            pos = (sx + dx, sy + dy)
            if (not dx) or (not dy):
                maze.walls.add(pos)
            else:
                maze.start[i] = pos
                i += 1


def maze_neighbour(func, max_nodes=5, cull_factor=1.6):
    best_dist = {}

    def f(node, current_dist):
        numkeys = len(node[0])
        best = best_dist.get(numkeys)
        if best is None or current_dist < best:
            best_dist[numkeys] = current_dist

        newbest = best_dist.get(numkeys + 1)
        cull = (newbest * cull_factor) if newbest else 0

        keys = set(node[0])
        nodes = sorted(func(node, current_dist))
        for dist, key, *state in nodes[:max_nodes]:
            if cull and dist > cull:
                continue
            yield (''.join(sorted({key} | keys)), *state), dist

    return f


if __name__ == '__main__':
    with open('input/18.txt') as f:
        maze = Maze(line.strip() for line in f)

    def found(node, distances):
        return len(node[0]) == maze.numkeys

    # part 1
    maze.compute_graph()
    free_keys = sum(1 for d, k in maze.graph[0].values() if not k)

    @maze_neighbour
    def simple(node, current_dist):
        keys = set(node[0])
        for key, info in maze.graph[node[1]].items():
            if key in keys or (info[1] - keys):
                continue
            yield (current_dist + info[0], key, key)

    dists_1 = dijkstra(('', 0), simple, stop=found)
    min_d = min(d for s, d in dists_1.items() if found(s, d))
    print(min_d)

    # part 2
    update_for_part_2(maze)
    maze.compute_graph()

    @maze_neighbour
    def robots(node, current_dist):
        keys = set(node[0])
        botpos = node[1:]
        for i, pos in enumerate(botpos):
            for key, info in maze.graph[pos].items():
                if key in keys or (info[1] - keys):
                    continue
                bots = list(botpos)
                bots[i] = key
                yield (current_dist + info[0], key, *bots)

    dists_2 = dijkstra(('', *maze.start), robots, stop=found)
    min_d = min(d for s, d in dists_2.items() if found(s, d))
    print(min_d)
