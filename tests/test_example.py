from app.logic import determine_result
from app.pathfinding import astar_graph

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

    # Correct Start
    assert result.path[0] == "0_0"

    # Correct End
    assert result.path[-1] == "1_1"

    # Cost > 0
    assert result.cost > 0

    # Path length
    assert len(result.path) >= 2


# logic.py

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

