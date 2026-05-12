RUNNER_SPEED = 26     # ft/s
FIELDER_SPEED = 23    # ft/s

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
    distance_ft = astar_cost      # 1 square = 1 ft
    return distance_ft / FIELDER_SPEED