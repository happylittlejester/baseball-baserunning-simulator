from drawing import draw_play
from field import BALL, PLAYERS, ball_in_bounds, generate_field_graph, to_node
from pathfinding import astar_graph, manhattan
from physics import fielder_time_to_ball, generate_base_times

width = 200
height = 200
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

# Time
base_times = generate_base_times()
fielder_time = fielder_time_to_ball(astar_result.cost)

if fielder_time < base_times["1B"]:
     print(f"Fielder was faster ({fielder_time:.2f}s vs runner {base_times['1B']:.2f}s)")
else:
    print(f"Runner reached base first ({base_times['1B']:.2f}s vs fielder {fielder_time:.2f}s)")


# Result
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