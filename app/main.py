import math

from drawing import draw_play
from field import BALL, BASES, PLAYERS, ball_in_bounds, generate_field_graph, to_node
from pathfinding import astar_graph, manhattan
from physics import fielder_total_time, generate_base_times

width = 350
height = 350
graph = generate_field_graph(width, height)

# HOME RUN if ball outside field
if not ball_in_bounds(BALL, width, height):
    print("HOME RUN")
    draw_play("HOME RUN")
    exit()

# OUT if ball lands on outfielder
for name, (px, py) in PLAYERS.items():
    if (px, py) == BALL:
        print("OUT! Ball caught by", name)
        draw_play("OUT")
        exit()

# A* - Closest outfielder
results = {}

for name, pos in PLAYERS.items():
    start = to_node(*pos)
    goal = to_node(*BALL)
    result = astar_graph(graph, start, goal, heuristic=lambda node, g=goal: manhattan(node, g))
    if result.cost is not None:
        results[name] = result.cost


best_player = min(results, key=results.get)
print("Fastest outfielder:", best_player)


start = to_node(*PLAYERS[best_player])
goal = to_node(*BALL)
astar_result = astar_graph(graph, start, goal, heuristic=lambda node: manhattan(node, goal))

print(astar_result)


if not results:
    print("No reachable players — ball too far.")
    draw_play("NO PLAY — BALL UNREACHABLE")
    exit()


# Throw distance from closest outfielder
throw_distances = {
    base: math.dist(BALL, pos)
    for base, pos in BASES.items()
}


# Time
base_times = generate_base_times()

fielder_times = {
    base: fielder_total_time(astar_result.cost, throw_distances[base])
    for base in BASES
}


for base in ["1B", "2B", "3B", "HOME"]:
    if fielder_times[base] < base_times[base]:
        print(f"Fielder was faster ({fielder_times[base]:.2f}s vs runner {base_times[base]:.2f}s) at {base}")
    else:
        print(f"Runner reached base first ({base_times[base]:.2f}s vs fielder {fielder_times[base]:.2f}s) at {base}")


# Result

# 1B
if base_times["1B"] >= fielder_times["1B"]:
    draw_play("OUT AT FIRST", outfielder=best_player, path=astar_result.path)
    exit()

# 2B
if base_times["2B"] >= fielder_times["2B"]:
    draw_play("SINGLE", highlight_base="1B", path=astar_result.path)
    exit()

# 3B
if base_times["3B"] >= fielder_times["3B"]:
    draw_play("DOUBLE", highlight_base="2B", path=astar_result.path)
    exit()

# HOME
if base_times["HOME"] >= fielder_times["HOME"]:
    draw_play("TRIPLE", highlight_base="3B", path=astar_result.path)
    exit()


draw_play("INSIDE THE PARK HOME RUN", path=astar_result.path)