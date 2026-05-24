from __future__ import annotations

import heapq
from dataclasses import dataclass
from typing import Callable

Graph = dict[str, list[tuple[str, int]]]

# Stores the result of an A* search: final path, visited nodes and total cost
@dataclass
class SearchResult:
    path: list
    visited_count: int
    cost: int | None = None


# Reconstructs the final path by backtracking from the goal to the start
def reconstruct_path(parent: dict, goal):
    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent.get(current)

    path.reverse()
    return path


# Manhattan heuristic (distance in vertical & horizontal steps)
def manhattan(a: str, b: str) -> int:
    ax, ay = map(int, a.split("_"))
    bx, by = map(int, b.split("_"))
    return abs(ax - bx) + abs(ay - by)


# A* pathfinding using Manhattan heuristic
def astar_graph(
    graph: Graph,
    start: str,
    goal: str,
    heuristic: Callable[[str], int],
    draw_graphs: bool = False
) -> SearchResult:
    queue = []
    heapq.heappush(queue, (0, start))

    visited = set()
    parent = {start: None}
    g_cost = {start: 0}
    visited_count = 0

    while queue:
        f_cost, node = heapq.heappop(queue)

        if node in visited:
            continue

        visited.add(node)
        visited_count += 1

        if node == goal:
            path = reconstruct_path(parent, goal)
            return SearchResult(path=path, visited_count=visited_count, cost=g_cost[node])

        for neighbor, weight in graph.get(node, []):
            tentative_g = g_cost[node] + weight

            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g
                parent[neighbor] = node
                f = tentative_g + heuristic(neighbor)
                heapq.heappush(queue, (f, neighbor))

    return SearchResult(path=[], visited_count=0, cost=None)