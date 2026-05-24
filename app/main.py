import math

from drawing import draw_play
from field import BALL, BASES, PLAYERS, ball_in_bounds, generate_field_graph, to_node
from logic import determine_result
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


# A* search for each outfielder to find who reaches the ball fastest
results = {}

for name, pos in PLAYERS.items():
    start = to_node(*pos)
    goal = to_node(*BALL)
    
    # Run A* with Manhattan heuristic
    result = astar_graph(graph, start, goal, heuristic=lambda node, g=goal: manhattan(node, g))
    
    # Store only valid results (reachable paths)
    if result.cost is not None:
        results[name] = result.cost


# Select the outfielder with the lowest A* path cost
best_player = min(results, key=results.get)
print("Fastest outfielder:", best_player)


# Run A* again for the chosen outfielder to get the final path
start = to_node(*PLAYERS[best_player])
goal = to_node(*BALL)
astar_result = astar_graph(graph, start, goal, heuristic=lambda node: manhattan(node, goal))

print(astar_result)

# If no player can reach the ball, show unreachable play
if not results:
    print("No reachable players — ball too far.")
    draw_play("NO PLAY — BALL UNREACHABLE")
    exit()


# Straight‑line throw distance (Euclidean)
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

# Compares runner and fielder times for each base
for base in ["1B", "2B", "3B", "HOME"]:
    if fielder_times[base] < base_times[base]:
        print(f"Fielder was faster ({fielder_times[base]:.2f}s vs runner {base_times[base]:.2f}s) at {base}")
    else:
        print(f"Runner reached base first ({base_times[base]:.2f}s vs fielder {fielder_times[base]:.2f}s) at {base}")


# Result
result = determine_result(base_times, fielder_times)

highlight_map = {
    "SINGLE": "1B",
    "DOUBLE": "2B",
    "TRIPLE": "3B"
}

highlight = highlight_map.get(result)

draw_play(result, highlight_base=highlight, path=astar_result.path)