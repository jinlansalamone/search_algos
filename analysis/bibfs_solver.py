from collections import deque

from environment import Environment, Coord


def bibfs_pathfind(environment):
    """
    Bi-directional Breadth-first search
    https://en.wikipedia.org/wiki/Bidirectional_search
    
    Returns (path, stats)

    path: list of coordinates from start to target inclusive, or None if no path.
    stats: dict with keys 'nodes_visited' and 'path_length'.
    """
    start = environment.start
    target = environment.find_target()
    if target is None:
        return None, {"nodes_visited": 0, "path_length": 0}

    if start == target:
        return [start], {"nodes_visited": 1, "path_length": 1}

    q_start = deque([start])
    q_target = deque([target])
    came_from_start = {start: None}
    came_from_target = {target: None}

    visited_count = 0
    meet = None

    def expand_frontier(queue, came_from, other_seen):
        nonlocal visited_count
        for _ in range(len(queue)):
            current = queue.popleft()
            visited_count += 1
            if current in other_seen:
                return current
            for neighbor in environment.get_adjacent(*current):
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    queue.append(neighbor)
        return None

    while q_start and q_target and meet is None:
        meet = expand_frontier(q_start, came_from_start, came_from_target)
        if meet is not None:
            break
        meet = expand_frontier(q_target, came_from_target, came_from_start)

    if meet is None:
        return None, {"nodes_visited": visited_count, "path_length": 0}

    # reconstruct path from start to meet
    path_start = []
    cur = meet
    while cur is not None:
        path_start.append(cur)
        cur = came_from_start[cur]
    path_start.reverse()

    # reconstruct path from meet to target
    path_target = []
    cur = came_from_target[meet]
    while cur is not None:
        path_target.append(cur)
        cur = came_from_target[cur]

    path = path_start + path_target

    return path, {"nodes_visited": visited_count, "path_length": len(path)}