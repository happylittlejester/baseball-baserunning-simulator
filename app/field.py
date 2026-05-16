import random

Graph = dict[str, list[tuple[str, int]]]

# Positions
BASES = {
    "1B": (90, 0),
    "2B": (90, 90),
    "3B": (0, 90),
    "HOME": (0, 0),
}

PLAYERS = {
    "LF": (80, 280),
    "CF": (300, 300),
    "RF": (270, 80),
}

# Generates a field grid
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


# Generates a random ball landing position
def generate_hit():
    while True:
        x = random.randint(0, 400) # noqa: S311
        y = random.randint(0, 400) # noqa: S311

        # Accepts only positions outside the diamond
        if (x, y) not in BASES.values() and not (0 <= x <= 90 and 0 <= y <= 90):
            return (x, y)


# Randomly generated ball position
BALL = generate_hit()
print("Ball landed at:", BALL)


# Checks if the ball is inside the field boundaries
def ball_in_bounds(ball, width, height):
    x, y = ball
    return 0 <= x < width and 0 <= y < height


# Converts (x, y) coordinates into a graph node string "x_y"
def to_node(x, y):
    return f"{x}_{y}"