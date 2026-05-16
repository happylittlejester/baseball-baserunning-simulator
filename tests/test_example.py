from app.logic import determine_result
from app.pathfinding import astar_graph
from app.physics import fielder_total_time, generate_base_times

# pathfinding.py

def test_astar():

    # Graph 2x2
    graph = {
        "0_0": [("1_0", 1), ("0_1", 1)],
        "1_0": [("1_1", 1), ("0_0", 1)],
        "0_1": [("0_0", 1), ("1_1", 1)],
        "1_1": []
    }

    # Manhattan
    def heuristic(node):
        x, y = map(int, node.split("_"))
        return abs(x - 1) + abs(y - 1)

    result = astar_graph(graph, "0_0", "1_1", heuristic)

    # Path found
    assert result.path

    # Path starts at the correct start node
    assert result.path[0] == "0_0"

    # Path ends at the correct goal node
    assert result.path[-1] == "1_1"

    # Path cost is positive
    assert result.cost > 0

    # Path contains at least two nodes
    assert len(result.path) >= 2


# logic.py

# determine_result returns the correct outcome based on which base the fielder reaches first

def test_out_at_first():
    base = {"1B": 4, "2B": 8, "3B": 12, "HOME": 16}
    field = {"1B": 3, "2B": 7, "3B": 11, "HOME": 15}
    assert determine_result(base, field) == "OUT AT FIRST"

def test_single():
    base = {"1B": 3, "2B": 10, "3B": 20, "HOME": 30}
    field = {"1B": 4, "2B": 5, "3B": 6, "HOME": 7}
    assert determine_result(base, field) == "SINGLE"

def test_double():
    base = {"1B": 3, "2B": 6, "3B": 9, "HOME": 12}
    field = {"1B": 4, "2B": 7, "3B": 5, "HOME": 13}
    assert determine_result(base, field) == "DOUBLE"

def test_triple():
    base =  {"1B": 3, "2B": 6, "3B": 9, "HOME": 12}
    field = {"1B": 4, "2B": 7, "3B": 10, "HOME": 8}
    assert determine_result(base, field) == "TRIPLE"

def test_inside_the_park_home_run():
    base =  {"1B": 3, "2B": 6, "3B": 9, "HOME": 12}
    field = {"1B": 5, "2B": 8, "3B": 11, "HOME": 20}
    assert determine_result(base, field) == "INSIDE THE PARK HOME RUN"


# physics.py

# All expected base keys are returned
def test_generate_base_times_keys():
    times = generate_base_times()
    assert set(times.keys()) == {"1B", "2B", "3B", "HOME"}

# All generated times are positive
def test_generate_base_times_positive():
    times = generate_base_times()
    for t in times.values():
        assert t > 0

# Time increases with distance
def test_generate_base_times_increasing():
    times = generate_base_times()
    assert times["1B"] < times["2B"] < times["3B"] < times["HOME"]

# Total fielder time is positive
def test_fielder_total_time_positive():
    t = fielder_total_time(100, 200)
    assert t > 0

# Longer distance results in longer time
def test_fielder_total_time_distance_effect():
    t1 = fielder_total_time(50, 50)
    t2 = fielder_total_time(100, 100)
    assert t2 > t1
