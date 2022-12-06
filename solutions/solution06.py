from collections import deque
from typing import Deque

import solutions

example = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"


def distinct_buffer(letter_sequence: str, buffer_length: int) -> int:
    buffer: Deque = deque([], buffer_length)
    indistinct = True
    i = 0
    while indistinct:
        buffer.append(letter_sequence[i])
        i += 1
        indistinct = len(set(buffer)) < buffer_length
    return i


assert distinct_buffer(example, 4) == 7
assert distinct_buffer(example, 14) == 19

with open("outputs/output06.txt", "w") as file:
    file.write(str(distinct_buffer(solutions.read_input("06"), 4)))
    file.write("\n")
    file.write(str(distinct_buffer(solutions.read_input("06"), 14)))
