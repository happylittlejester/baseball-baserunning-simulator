def determine_result(base_times, fielder_times):
    if fielder_times["1B"] < base_times["1B"]:
        return "OUT AT FIRST"

    if fielder_times["2B"] < base_times["2B"]:
        return "SINGLE"

    if fielder_times["3B"] < base_times["3B"]:
        return "DOUBLE"

    if fielder_times["HOME"] < base_times["HOME"]:
        return "TRIPLE"

    return "INSIDE THE PARK HOME RUN"