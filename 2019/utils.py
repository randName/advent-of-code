def dijkstra(src, neighbours, dst=None):
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
                distances[node] = newdist
        if current == dst:
            break
        visited.add(current)
        unvisited = distances.keys() - visited

    if dst is not None:
        return distances[dst]
    return distances
