import random

Graph = dict[str, list[tuple[str, int]]]

# Positions
BASES = {
    "home": (0, 0),
    "first": (90, 0),
    "second": (90, 90),
    "third": (0, 90),
}

PLAYERS = {
    "LF": (50, 180),
    "CF": (170, 175),
    "RF": (180, 50),
}

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


def generate_hit():
    while True:
        x = random.randint(0, 220) # noqa: S311
        y = random.randint(0, 220) # noqa: S311

        if (x, y) not in BASES.values() and not (0 <= x <= 90 and 0 <= y <= 90):
            return (x, y)


BALL = generate_hit()
print("Ball landed at:", BALL)


def ball_in_bounds(ball, width, height):
    x, y = ball
    return 0 <= x < width and 0 <= y < height


def to_node(x, y):
    return f"{x}_{y}"