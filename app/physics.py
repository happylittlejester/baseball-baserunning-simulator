RUNNER_SPEED = 24     # ft/s
FIELDER_SPEED = 22    # ft/s
FIELDER_THROW = 65    # mph


def runner_time_to(distance):
    return distance / RUNNER_SPEED


def generate_base_times():
    return {
        "1B": runner_time_to(90),
        "2B": runner_time_to(180),
        "3B": runner_time_to(270),
        "HOME": runner_time_to(360),
    }


def throw_time(distance_ft):
    velocity = FIELDER_THROW * 1.46667  # mph → ft/s
    return distance_ft / velocity


def fielder_total_time(run_distance_ft, throw_distance_ft):
    time_to_ball = run_distance_ft / FIELDER_SPEED
    time_throw = throw_time(throw_distance_ft)
    return time_to_ball + time_throw