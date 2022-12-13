from typing import List, Optional

import solutions

example = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


def parse_outer(secretly_list: str) -> List[str]:
    assert (secretly_list[0] == "[") and (secretly_list[-1] == "]"), f"got {secretly_list}"
    listified = []
    level = 0
    current_item = ""
    for character in secretly_list[1:-1]:
        if level == 0 and character == ",":
            listified.append(current_item)
            current_item = ""
        else:
            current_item += character
        if character == "[":
            level += 1
        elif character == "]":
            level -= 1
    listified.append(current_item)
    return listified


def compare_pairs(left: List[str], right: List[str]) -> Optional[bool]:
    if (not left) or (not right):
        return None if (not left) and (not right) else bool(right)
    left_current = left[0]
    right_current = right[0]
    if (not left_current) or (not right_current):
        return None if (not left_current) and (not right_current) else bool(right_current)
    elif (left_current[0] == "[") or (right_current[0] == "["):
        left_inner = parse_outer(left_current if left_current[0] == "[" else ("[" + left_current + "]"))
        right_inner = parse_outer(right_current if right_current[0] == "[" else ("[" + right_current + "]"))
        if compare_pairs(left_inner, right_inner) is None:
            return compare_pairs(left[1:], right[1:])
        else:
            return compare_pairs(left_inner, right_inner)
    else:
        if int(left_current) == int(right_current):
            if left[1:] and right[1:]:
                return compare_pairs(left[1:], right[1:])
            elif left[1:] or right[1:]:
                return bool(right[1:])
        else:
            return int(left_current) < int(right_current)


example_answers = [True, True, False, True, False, True, False, False]
example_num = 0

for pair in example.split("\n\n"):
    left, right = tuple(pair.splitlines())
    assert compare_pairs(parse_outer(left), parse_outer(right)) == example_answers[example_num]
    example_num += 1


def indices_of_ordered(pairs: str) -> int:
    indices = []
    pair_num = 1
    for pair in pairs.split("\n\n"):
        left, right = tuple(pair.splitlines())
        if compare_pairs(parse_outer(left), parse_outer(right)):
            indices.append(pair_num)
        pair_num += 1
    return sum(indices)


assert indices_of_ordered(example) == 13


def specified_placement(pairs: str) -> int:
    extra_packets = {"[[2]]": 1, "[[6]]": 1}
    for row in [line for line in pairs.splitlines() if line]:
        for key in extra_packets:
            if compare_pairs(parse_outer(row), parse_outer(key)):
                extra_packets[key] += 1
    return extra_packets["[[2]]"] * (extra_packets["[[6]]"] + 1)


assert specified_placement(example) == 140

with open("outputs/output13.txt", "w") as file:
    input = solutions.read_input("13")
    file.write(str(indices_of_ordered(input)))
    file.write("\n")
    file.write(str(specified_placement(input)))
