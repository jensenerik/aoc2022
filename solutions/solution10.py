from typing import List

import solutions

tiny_example = """noop
addx 3
addx -5"""

example = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""


def single_command(command: str) -> int:
    if command == "noop":
        return 0
    else:
        return int(command.split()[1])


def parse_commands(commands: str) -> List[int]:
    return [single_command(command) for command in commands.splitlines()]


def add_history(commands: List[int]) -> List[int]:
    total_cycles = 2 * len(commands) - commands.count(0)
    cycle_history = [1] + ([0] * total_cycles)
    current_cycle = 0
    for command in commands:
        if command == 0:
            current_cycle += 1
        else:
            cycle_history[current_cycle + 2] = command
            current_cycle += 2
    return cycle_history


def signal(commands: List[int], cycle: int) -> int:
    return cycle * (sum(add_history(commands)[: cycle]))  # fmt: skip


def signal_sum(commands: str) -> int:
    return sum(signal(parse_commands(commands), cycle) for cycle in [20, 60, 100, 140, 180, 220])


assert signal_sum(example) == 13140


def register_history(add_history: List[int]) -> List[int]:
    return [sum(add_history[:i]) for i, _ in enumerate(add_history)]


def crt_data(register_history: List[int]) -> List[bool]:
    return [(abs(register - (i % 40)) <= 1) for i, register in enumerate(register_history[1:])]


def crt_pixel(crt_data: List[bool]) -> str:
    pixel_map = {True: "#", False: "."}
    return "".join([pixel_map[item] for item in crt_data])


def crt_display(commands: str) -> str:
    data = crt_data(register_history(add_history(parse_commands(commands))))
    output = ""
    for left_position in range(0, len(data), 40):
        output = output + crt_pixel(data[left_position: left_position + 40]) + "\n"  # fmt: skip
    return output


crt = crt_data(register_history(add_history(parse_commands(example))))
assert crt[:40] == (([True] * 2) + ([False] * 2)) * 10
assert crt[40:80] == (([True] * 3) + ([False] * 3)) * 6 + [True] * 3 + [False]
assert crt[80:120] == (([True] * 4) + ([False] * 4)) * 5

with open("outputs/output10.txt", "w") as file:
    input = solutions.read_input("10")
    file.write(str(signal_sum(input)))
    file.write("\n")
    file.writelines(crt_display(input))
