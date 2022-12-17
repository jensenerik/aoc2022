from typing import List, Optional, Set, Tuple

import solutions

rock_types = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##"""

example = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"


def split_rock_types(rock_types: str) -> List[Set[Tuple[int, int]]]:
    output = []
    for rock in rock_types.split("\n\n"):
        rock_coords: Set[Tuple[int, int]] = set()
        rock_lines = rock.splitlines()
        height = len(rock_lines)
        for i, row in enumerate(rock_lines):
            rock_coords.update({(j, height - i - 1) for j, pixel in enumerate(row) if pixel == "#"})
        output.append(rock_coords)
    return output


def highest_point(rock_pattern: Set[Tuple[int, int]]) -> int:
    return max([coord[1] for coord in rock_pattern]) if rock_pattern else -1


def add_coords(coord_1: Tuple[int, int], coord_2: Tuple[int, int]) -> Tuple[int, int]:
    return (coord_1[0] + coord_2[0], coord_1[1] + coord_2[1])


def hit_walls(coord: Tuple[int, int], left_wall: int, right_wall: int) -> bool:
    return (coord[0] <= left_wall) or (coord[0] >= right_wall) or (coord[1] < 0)


def drop_rock(
    rock_state: Set[Tuple[int, int]], new_rock: Set[Tuple[int, int]], jet_seq: str, jet_seq_start: int
) -> Tuple[Set[Tuple[int, int]], int]:
    timer = 0
    base_offset = (2, highest_point(rock_state) + 4)
    current_spot = {add_coords(rock_pixel, base_offset) for rock_pixel in new_rock}
    jet_seq_num = jet_seq_start
    floor_collision = False
    while not floor_collision:
        if timer % 2 == 0:
            shift = (1, 0) if jet_seq[jet_seq_num] == ">" else (-1, 0)
            jet_seq_num = (jet_seq_num + 1) % len(jet_seq)
        else:
            shift = (0, -1)
        new_spot = {add_coords(rock_pixel, shift) for rock_pixel in current_spot}
        if new_spot.isdisjoint(rock_state) and not max([hit_walls(coord, -1, 7) for coord in new_spot]):
            current_spot = new_spot
        elif timer % 2 == 1:
            floor_collision = True
        timer += 1
    return (rock_state.union(current_spot), jet_seq_num)


def drop_many_rocks(rock_types: str, jet_seq: str, stopping_point: int) -> Tuple[int, List[int]]:
    rock_type_coords = split_rock_types(rock_types)
    rock_num = 0
    rock_state: Set[Tuple[int, int]] = set()
    jet_seq_num = 0
    height_sequence = [0]
    while rock_num < stopping_point:
        rock_state, jet_seq_num = drop_rock(rock_state, rock_type_coords[rock_num % 5], jet_seq, jet_seq_num)
        rock_num += 1
        if rock_num % 5 == 0:
            height_sequence.append(highest_point(rock_state) + 1)
    return (
        highest_point(rock_state) + 1,
        [height - height_sequence[i - 1] for i, height in enumerate(height_sequence) if i > 0],
    )


def deja_vu(height_sequence: List[int]) -> Optional[int]:
    for i in range(10, len(height_sequence) // 2):
        if height_sequence[-i:] == height_sequence[-i * 2 : -i]:
            return i
    return None


def extrapolate_rocks(rock_types: str, jet_seq: str, stopping_point: int, early_num: int) -> Optional[int]:
    early_peak, early_seq = drop_many_rocks(rock_types, jet_seq, early_num)
    deja_vu_num = deja_vu(early_seq)
    if deja_vu_num:
        repeat_sum = sum(early_seq[-deja_vu_num:])
        extra = sum(early_seq[-deja_vu_num : -deja_vu_num + (((stopping_point - early_num) // 5) % deja_vu_num)])
        return early_peak + (repeat_sum * ((stopping_point - early_num) // (5 * deja_vu_num))) + extra
    return None


LARGE_ROCK_QUANTITY = 1000000000000

big_answer = extrapolate_rocks(rock_types, example, LARGE_ROCK_QUANTITY, 500)
assert big_answer == 1514285714288, f"got {big_answer}"


with open("outputs/output17.txt", "w") as file:
    daily_input = solutions.read_input("17")
    file.write(str(drop_many_rocks(rock_types, daily_input, 2022)[0]))
    # 21 seconds to do 10,000 rocks with naive approach
    file.write("\n")
    file.write(str(extrapolate_rocks(rock_types, daily_input, LARGE_ROCK_QUANTITY, 5000)))
