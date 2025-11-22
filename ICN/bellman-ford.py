# Bellman-Ford Algorithm in Python
# Finds shortest distances and the path from a source vertex

def bellman_ford(vertices, edges, source):
    # Step 1: Initialize distances
    distance = {v: float('inf') for v in vertices}
    parent = {v: None for v in vertices}
    distance[source] = 0

    # Step 2: Relax edges |V|-1 times
    for _ in range(len(vertices) - 1):
        for u, v, w in edges:
            if distance[u] + w < distance[v]:
                distance[v] = distance[u] + w
                parent[v] = u

    # Step 3: Check for negative weight cycles
    for u, v, w in edges:
        if distance[u] + w < distance[v]:
            print("Negative weight cycle detected!")
            return None, None

    return distance, parent


def get_path(parent, target):
    """ Reconstruct path from source to target """
    path = []
    while target is not None:
        path.append(target)
        target = parent[target]
    return path[::-1]  # reverse


# Example Usage
if __name__ == "__main__":
    # Define vertices
    vertices = ['A', 'B', 'C', 'D', 'E']

    # Define edges as (u, v, weight)
    edges = [
        ('A', 'B', 6),
        ('A', 'D', 7),
        ('B', 'C', 5),
        ('B', 'D', 8),
        ('B', 'E', -4),
        ('C', 'B', -2),
        ('D', 'C', -3),
        ('D', 'E', 9),
        ('E', 'A', 2),
        ('E', 'C', 7)
    ]

    source = 'A'
    target = 'E'

    distance, parent = bellman_ford(vertices, edges, source)

    if distance:
        print("Shortest distances from source:", distance)
        print(f"Shortest path from {source} to {target}: {get_path(parent, target)}")
