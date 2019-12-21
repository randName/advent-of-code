class Paths:

    def __init__(self, tree):
        self.tree = tree

    def __getitem__(self, key):
        return tuple(reversed(tuple(self.walk(key))))

    def walk(self, key):
        while key:
            key = self.tree.get(key)
            if key:
                yield key

    def __repr__(self):
        return '<Paths(%d)>' % len(self.tree)


def dijkstra(src, neighbours, dst=None, stop=None, paths=False):
    parents = {}
    visited = set()
    unvisited = {src}
    distances = {src: 0}

    def dist(key):
        return distances[key]

    while unvisited:
        current = min(unvisited, key=dist)
        for node, newdist in neighbours(current, distances[current]):
            olddist = distances.get(node)
            if olddist is None or newdist < olddist:
                parents[node] = current
                distances[node] = newdist

        if current == dst:
            break

        try:
            if stop(current, distances):
                break
        except TypeError:
            pass

        visited.add(current)
        unvisited = distances.keys() - visited

    if dst is not None:
        return distances[dst]

    if paths:
        return distances, Paths(parents)

    return distances
