from collections import deque
from environment import Environment, Coord


def bfs_pathfind(environment):
    """
    Returns (path, stats).

    path: list of coordinates from start to target inclusive, or None if no path.
    stats: dict with keys 'nodes_visited' and 'path_length'.
    """
    start = environment.start
    target = environment.find_target()
    if target is None:
        return None, {"nodes_visited": 0, "path_length": 0}

    queue = deque([start])
    came_from = {start: None}
    visited_count = 0

    while queue:
        y, x = queue.popleft()
        visited_count += 1

        if (y, x) == target:
            break

        for ny, nx in environment.get_adjacent(y, x):
            if (ny, nx) not in came_from:
                came_from[(ny, nx)] = (y, x)
                queue.append((ny, nx))

    if target not in came_from:
        return None, {"nodes_visited": visited_count, "path_length": 0}

    # Reconstruct path
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()

    return path, {"nodes_visited": visited_count, "path_length": len(path)}