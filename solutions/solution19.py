from typing import Dict, List, NamedTuple, Set

import solutions

example = (
    "Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. "
    "Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.\n"
    "Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. "
    "Each geode robot costs 3 ore and 12 obsidian."
)


class Robot(NamedTuple):
    robot_type: str
    robot_cost: Dict[str, int]


class Blueprint(NamedTuple):
    blueprint_num: int
    robots: Dict[str, Robot]


def parse_robot(robot_text: str) -> Robot:
    split_text = robot_text.split()
    robot_type = split_text[0]
    if len(split_text) == 5:
        robot_cost = {split_text[4][:-1]: int(split_text[3])}
    else:
        robot_cost = {split_text[4]: int(split_text[3]), split_text[7][:-1]: int(split_text[6])}
    return Robot(robot_type, robot_cost)


def parse_blueprint(blueprint_text: str) -> List[Blueprint]:
    blueprints = []
    for blueprint in blueprint_text.splitlines():
        robot_text = blueprint.split("Each ")
        blueprint_num = int(robot_text[0][len("Blueprint ") : -2])
        blueprints.append(
            Blueprint(blueprint_num, {parse_robot(robot).robot_type: parse_robot(robot) for robot in robot_text[1:]})
        )
    return blueprints


class RobotState:
    time_step: int
    stockpile: Dict[str, int]
    robot_counts: Dict[str, int]
    declined_choices: Set[str]

    def __init__(
        self, time_step: int, stockpile: Dict[str, int], robot_counts: Dict[str, int], declined_choices: Set[str]
    ):
        self.time_step = time_step
        self.stockpile = stockpile
        self.robot_counts = robot_counts
        self.declined_choices = declined_choices

    def __repr__(self):
        return str([self.time_step, self.stockpile, self.robot_counts, self.declined_choices])

    def possibilities(self, blueprint: Blueprint) -> Set[str]:
        possibilities = {"pass"}
        for robot in blueprint.robots.values():
            if min([self.stockpile[resource] - cost for resource, cost in robot.robot_cost.items()]) >= 0:
                possibilities.add(robot.robot_type)
        return possibilities.difference(self.declined_choices)


def cold_start() -> RobotState:
    return RobotState(
        0,
        {resource: 0 for resource in ["ore", "clay", "obsidian", "geode"]},
        {"ore": 1} | {robot: 0 for robot in ["clay", "obsidian", "geode"]},
        set(),
    )


def next_states(current_state: RobotState, blueprint: Blueprint) -> List[RobotState]:
    new_states: List[RobotState] = []
    for next_step in current_state.possibilities(blueprint):
        new_time_step = current_state.time_step + 1
        if next_step == "pass":
            new_robot_state = RobotState(
                new_time_step,
                {
                    resource: current_value + current_state.robot_counts[resource]
                    for resource, current_value in current_state.stockpile.items()
                },
                current_state.robot_counts,
                current_state.declined_choices.union(current_state.possibilities(blueprint)).difference(["pass"]),
            )
        else:
            new_robot_state = RobotState(
                new_time_step,
                {
                    resource: current_value
                    + current_state.robot_counts[resource]
                    - blueprint.robots[next_step].robot_cost.get(resource, 0)
                    for resource, current_value in current_state.stockpile.items()
                },
                {
                    robot_type: current_count + (1 if robot_type == next_step else 0)
                    for robot_type, current_count in current_state.robot_counts.items()
                },
                set(),
            )
        if len(new_robot_state.declined_choices) < 4:
            new_states.append(new_robot_state)
    return new_states


def state_score(robot_state: RobotState, time_limit: int) -> int:
    expected_values = {
        resource: stockpile_value + robot_state.robot_counts[resource] * (time_limit - robot_state.time_step)
        for resource, stockpile_value in robot_state.stockpile.items()
    }
    fixed_multiplier = 10

    return sum(
        [
            expected_values["geode"] * fixed_multiplier**10,
            expected_values["obsidian"] * fixed_multiplier**5,
            expected_values["clay"] * fixed_multiplier**3,
            expected_values["ore"] * fixed_multiplier**0,
        ]
    )


def most_geodes(blueprint: Blueprint, time_limit: int) -> int:
    current_states: Set[RobotState] = {cold_start()}
    new_states: Set[RobotState] = set()
    for time_step in range(time_limit):
        for state in current_states:
            new_states.update(next_states(state, blueprint))
        current_states = set(sorted(new_states, key=lambda state: state_score(state, time_limit), reverse=True)[:1000])
        new_states = set()
    return max([state.stockpile["geode"] for state in current_states])


def quality_sum(instructions: str, time_limit: int) -> int:
    blueprints = parse_blueprint(instructions)
    total_sum = 0
    for blueprint in blueprints:
        total_sum += blueprint.blueprint_num * most_geodes(blueprint, time_limit)
    return total_sum


def geode_multipier(instructions: str, blueprint_limit: int, time_limit: int) -> int:
    blueprints = parse_blueprint(instructions)[:blueprint_limit]
    total_product = 1
    for blueprint in blueprints:
        total_product = total_product * most_geodes(blueprint, time_limit)
    return total_product


with open("outputs/output19.txt", "w") as file:
    daily_input = solutions.read_input("19")
    file.write(str(quality_sum(daily_input, 24)))
    file.write("\n")
    file.write(str(geode_multipier(daily_input, 3, 32)))
