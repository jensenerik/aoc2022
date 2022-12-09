from typing import List, Tuple

import solutions

example = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""


long_example = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""


def move_parse(moves: str) -> List[str]:
    expanded_moves = []
    for move in moves.split("\n"):
        expanded_moves.extend([move.split()[0]] * int(move.split()[1]))
    return expanded_moves


def translate_to_coord(coordinate: Tuple[int, int], move: str) -> Tuple[int, int]:
    if move == "R":
        return (coordinate[0] + 1, coordinate[1])
    if move == "L":
        return (coordinate[0] - 1, coordinate[1])
    if move == "U":
        return (coordinate[0], coordinate[1] + 1)
    if move == "D":
        return (coordinate[0], coordinate[1] - 1)
    else:
        raise Exception(f"unparseable move {move}")


def construct_move(relative_error: int):
    if relative_error == 0:
        return relative_error
    else:
        return relative_error // abs(relative_error)


def coord_follow(tail_coord: Tuple[int, int], head_coord: Tuple[int, int]) -> Tuple[int, int]:
    intermediate_head = (head_coord[0] - tail_coord[0], head_coord[1] - tail_coord[1])
    if {-1, 0, 1}.issuperset(intermediate_head):
        return tail_coord
    else:
        t_horiz_move = construct_move(intermediate_head[0])
        t_vert_move = construct_move(intermediate_head[1])
        return (tail_coord[0] + t_horiz_move, tail_coord[1] + t_vert_move)


def run_long_moveset(moves: str, rope_length: int) -> int:
    coords = [(0, 0)] * rope_length
    tail_trail = set()
    for move in move_parse(moves):
        coords[0] = translate_to_coord(coords[0], move)
        for i in range(1, rope_length):
            coords[i] = coord_follow(coords[i], coords[i - 1])
        tail_trail.add(coords[-1])
    return len(tail_trail)


assert run_long_moveset(example, 2) == 13
assert run_long_moveset(long_example, 10) == 36


with open("outputs/output09.txt", "w") as file:
    input = solutions.read_input("09")
    file.write(str(run_long_moveset(input, 2)))
    file.write("\n")
    file.write(str(run_long_moveset(input, 10)))
