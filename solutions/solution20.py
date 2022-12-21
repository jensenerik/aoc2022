from collections import deque

import solutions

example = """1
2
-3
3
-2
0
4"""


def move_guys(jump_list: str, part_2: bool = False):
    jumps = [int(row) for row in jump_list.splitlines()]
    if part_2:
        jumps = [jump * 811589153 for jump in jumps]
    stack_size = len(jumps)
    stack = deque(range(stack_size))
    for _ in range(10 if part_2 else 1):
        for i in range(stack_size):
            jump = jumps[i]
            deque_position = stack.index(i)
            stack.remove(i)
            uncorrected = (deque_position + (jump % (stack_size - 1))) % (stack_size)
            if uncorrected >= deque_position:
                stack.insert(uncorrected, i)
            else:
                stack.insert((uncorrected + 1) % (stack_size), i)
    stack.rotate(-stack.index(jumps.index(0)))
    return [jumps[i] for i in stack]


def calculate_grove_sum(num_seq: str, part_2: bool = False) -> int:
    final_positions = move_guys(num_seq, part_2)
    mod_size = len(final_positions)
    answers = [final_positions[x % mod_size] for x in [1000, 2000, 3000]]
    return sum(answers)


assert calculate_grove_sum(example) == 3

assert calculate_grove_sum(example, True) == 1623178306


with open("outputs/output20.txt", "w") as file:
    daily_input = solutions.read_input("20")
    file.write(str(calculate_grove_sum(daily_input)))
    file.write("\n")
    file.write(str(calculate_grove_sum(daily_input, True)))
