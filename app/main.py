from __future__ import annotations

import heapq
import random
from dataclasses import dataclass
from typing import Callable

import matplotlib.pyplot as plt

Graph = dict[str, list[tuple[str, int]]]

@dataclass
class SearchResult:
    path: list
    visited_count: int
    cost: int | None = None

def reconstruct_path(parent: dict, goal):
    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent.get(current)

    path.reverse()
    return path


# Field grid
def generate_field_graph(width: int, height: int) -> Graph:
    graph: Graph = {}

    for x in range(width):
        for y in range(height):
            node = f"{x}_{y}"
            neighbors = []

            if x > 0:
                neighbors.append((f"{x-1}_{y}", 1))
            if x < width - 1:
                neighbors.append((f"{x+1}_{y}", 1))
            if y > 0:
                neighbors.append((f"{x}_{y-1}", 1))
            if y < height - 1:
                neighbors.append((f"{x}_{y+1}", 1))

            graph[node] = neighbors

    return graph


def manhattan(a: str, b: str) -> int:
    ax, ay = map(int, a.split("_"))
    bx, by = map(int, b.split("_"))
    return abs(ax - bx) + abs(ay - by)


# Positions
BASES = {
    "home": (0, 0),
    "first": (90, 0),
    "second": (90, 90),
    "third": (0, 90),
}

PLAYERS = {
    "LF": (50, 150),
    "CF": (170, 160),
    "RF": (175, 50),
}

def random_outfield_point(max_x=250, max_y=250):
    while True:
        x = random.uniform(0, max_x) # noqa: S311
        y = random.uniform(0, max_y) # noqa: S311

        if not (0 <= x <= 90 and 0 <= y <= 90):
            return (int(x), int(y))

BALL = random_outfield_point()
print("Ball landed at:", BALL)

def to_node(x, y):
    return f"{x}_{y}"

def draw_field_path(path: list[str]):
    fig, ax = plt.subplots(figsize=(8, 8))

    # bases
    for name, (x, y) in BASES.items():
        ax.scatter(x, y, s=200, color="white", edgecolor="black")
        ax.text(x, y, name, ha="center", va="center")

    # outfielders
    for name, (x, y) in PLAYERS.items():
        ax.scatter(x, y, s=200, color="blue")
        ax.text(x, y, name, ha="center", va="center", color="white")

    # ball
    bx, by = BALL
    ax.scatter(bx, by, s=200, color="red")
    ax.text(bx, by, "ball", ha="center", va="center", color="white")

    # path
    xs = []
    ys = []
    for node in path:
        x, y = map(int, node.split("_"))
        xs.append(x)
        ys.append(y)

    ax.plot(xs, ys, color="yellow", linewidth=2)

    ax.set_xlim(-10, 200)
    ax.set_ylim(-10, 200)
    ax.set_aspect("equal")
    plt.show()


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


graph = generate_field_graph(200, 200)

results = {}

for name, pos in PLAYERS.items():
    start = to_node(*pos)
    goal = to_node(*BALL)

    result = astar_graph(
        graph,
        start,
        goal,
        heuristic=lambda node, g=goal: manhattan(node, g)
    )

    results[name] = result.cost

best_player = min(results, key=results.get)
print("Fastest player:", best_player)

start = to_node(*PLAYERS[best_player])
goal = to_node(*BALL)

astar_result = astar_graph(
    graph,
    start,
    goal,
    heuristic=lambda node: manhattan(node, goal)
)

print(astar_result)
draw_field_path(astar_result.path)