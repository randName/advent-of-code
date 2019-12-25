from heapq import heappop, heappush


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
    distances = {src: 0}

    queue = [(0, src)]

    while queue:
        cur_dist, current = heappop(queue)

        if current == dst:
            break

        if current in visited:
            continue
        visited.add(current)

        for node, newdist in neighbours(current, cur_dist):
            olddist = distances.get(node)
            if olddist is None or newdist < olddist:
                parents[node] = current
                distances[node] = newdist
                heappush(queue, (newdist, node))

        try:
            if stop(current, distances):
                break
        except TypeError:
            pass

    if dst is not None:
        return distances[dst]

    if paths:
        return distances, Paths(parents)

    return distances
