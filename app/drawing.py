import matplotlib.pyplot as plt
from field import BALL, BASES, PLAYERS


def draw_play(result_text, highlight_base=None, outfielder=None, path=None):
    fig, ax = plt.subplots(figsize=(8, 8))

    # bases
    for name, (x, y) in BASES.items():
        color = "green" if result_text == "HOME RUN" or name == highlight_base else "white"
        ax.scatter(x, y, s=200, color=color, edgecolor="black")
        ax.text(x, y, name, ha="center", va="center")

    # outfielders
    for name, (x, y) in PLAYERS.items():
        color = "blue"
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
    ax.text(200, 200, result_text, ha="center", va="center",
            fontsize=30, color="yellow", weight="bold")

    ax.set_xlim(-10, 350)
    ax.set_ylim(-10, 350)
    ax.set_aspect("equal")
    plt.show()