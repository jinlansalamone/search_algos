import heapq

from environment import Environment, Coord


def astar_pathfind(environment):
    """
    Returns (path, stats).

    path: list of coordinates from start to target inclusive, or None if no path.
    stats: dict with keys 'nodes_visited' and 'path_length'.
    """
    start = environment.start
    target = environment.find_target()
    if target is None:
        return None, {"nodes_visited": 0, "path_length": 0}

    def manhattan(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_heap = []
    heapq.heappush(open_heap, (manhattan(start, target), 0, start))

    came_from = {start: None}
    g_score = {start: 0}
    closed = set()
    visited_count = 0

    while open_heap:
        _, cur_g, current = heapq.heappop(open_heap)
        if current in closed:
            continue
        closed.add(current)
        visited_count += 1

        if current == target:
            break

        for neighbor in environment.get_adjacent(*current):
            if neighbor in closed:
                continue
            tentative_g = cur_g + 1
            if tentative_g < g_score.get(neighbor, 1 << 30):
                g_score[neighbor] = tentative_g
                came_from[neighbor] = current
                f_score = tentative_g + manhattan(neighbor, target)
                heapq.heappush(open_heap, (f_score, tentative_g, neighbor))

    if target not in came_from:
        return None, {"nodes_visited": visited_count, "path_length": 0}

    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()

    return path, {"nodes_visited": visited_count, "path_length": len(path)}