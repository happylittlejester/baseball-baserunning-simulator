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

def generate_hit():
    while True:
        x = random.randint(0, 220) # noqa: S311
        y = random.randint(0, 220) # noqa: S311

        if not (0 <= x <= 90 and 0 <= y <= 90):
            return (x, y)


BALL = generate_hit()
print("Ball landed at:", BALL)


RUNNER_SPEED = 26     # ft/s
FIELDER_SPEED = 24    # ft/s

def runner_time_to(distance):
    return distance / RUNNER_SPEED

def generate_base_times():
    return {
        "1B": runner_time_to(90),
        "2B": runner_time_to(180),
        "3B": runner_time_to(270),
        "HOME": runner_time_to(360),
    }

def fielder_time_to_ball(astar_cost):
    distance_ft = astar_cost      # 1 kratka = 1 ft
    return distance_ft / FIELDER_SPEED


def to_node(x, y):
    return f"{x}_{y}"

def draw_play(result_text, highlight_base=None, outfielder=None, path=None):
    fig, ax = plt.subplots(figsize=(8, 8))

    # bases
    for name, (x, y) in BASES.items():
        color = "green" if name == highlight_base else "white"
        ax.scatter(x, y, s=200, color=color, edgecolor="black")
        ax.text(x, y, name, ha="center", va="center")

    # outfielders
    for name, (x, y) in PLAYERS.items():
        color = "orange" if name == outfielder else "blue"
        ax.scatter(x, y, s=200, color=color)
        ax.text(x, y, name, ha="center", va="center", color="white")

    # ball
    bx, by = BALL
    ax.scatter(bx, by, s=200, color="red")
    ax.text(bx, by, "ball", ha="center", va="center", color="white")

    # path
    if path:
        xs, ys = [], []
        for node in path:
            x, y = map(int, node.split("_"))
            xs.append(x)
            ys.append(y)
        ax.plot(xs, ys, color="yellow", linewidth=2)

    # result text
    ax.text(100, 100, result_text, ha="center", va="center",
            fontsize=30, color="yellow", weight="bold")

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


width = 200
height = 200
graph = generate_field_graph(width, height)

def ball_in_bounds(ball, width, height):
    x, y = ball
    return 0 <= x < width and 0 <= y < height

# OUT if ball lands on outfielder
for name, (px, py) in PLAYERS.items():
    if (px, py) == BALL:
        print("OUT! Ball caught by", name)
        draw_play("OUT", outfielder=name, path=astar_result.path)
        exit()

# HOME RUN if ball outside field
if not ball_in_bounds(BALL, width, height):
    print("HOME RUN")
    draw_play("HOME RUN", path=astar_result.path)
else:
    results = {}

    for name, pos in PLAYERS.items():
        start = to_node(*pos)
        goal = to_node(*BALL)
        result = astar_graph(graph, start, goal, heuristic=lambda node, g=goal: manhattan(node, g))
        if result.cost is not None:
            results[name] = result.cost

    if not results:
        print("No reachable players — ball too far.")
    else:
        best_player = min(results, key=results.get)
        print("Fastest outfielder:", best_player)

        start = to_node(*PLAYERS[best_player])
        goal = to_node(*BALL)
        astar_result = astar_graph(graph, start, goal, heuristic=lambda node: manhattan(node, goal))
        print(astar_result)

        # czasy
        base_times = generate_base_times()
        fielder_time = fielder_time_to_ball(astar_result.cost)

        if fielder_time < base_times["1B"]:
            print(f"Fielder was faster ({fielder_time:.2f}s vs runner {base_times['1B']:.2f}s)")
        else:
            print(f"Runner reached base first ({base_times['1B']:.2f}s vs fielder {fielder_time:.2f}s)")


        if base_times["HOME"] < fielder_time:
            draw_play("INSIDE THE PARK HOME RUN", path=astar_result.path)

        elif base_times["3B"] < fielder_time:
            draw_play("TRIPLE", highlight_base="third", path=astar_result.path)

        elif base_times["2B"] < fielder_time:
            draw_play("DOUBLE", highlight_base="second", path=astar_result.path)

        elif base_times["1B"] < fielder_time:
            draw_play("SINGLE", highlight_base="first", path=astar_result.path)

        else:
            draw_play("OUT AT FIRST", outfielder=best_player, path=astar_result.path)