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

