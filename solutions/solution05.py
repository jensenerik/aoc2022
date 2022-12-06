from typing import Dict, List, Tuple

import solutions

example = """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
""".strip(  # noqa: W291
    "\n"
)


def parse_stacks(stack_diagram: str) -> Dict[int, List]:
    stacks = [row for row in zip(*stack_diagram.split("\n")) if row[-1].strip()]
    return {int(stack[-1]): [box for box in stack[-2::-1] if box.strip()] for stack in stacks}


def single_move_parse(text_move: List[str]) -> List[Tuple[int, int]]:
    return [(int(text_move[3]), int(text_move[5]))] * int(text_move[1])


def parse_moves(moveset: str) -> List[Tuple[int, int]]:
    text_moves = [row.split() for row in moveset.split("\n")]
    simple_moves = []
    for row in text_moves:
        simple_moves.extend(single_move_parse(row))
    return simple_moves


def parse_data(problem_input: str) -> Tuple[Dict[int, List], List[Tuple[int, int]]]:
    diagram, moves = problem_input.split("\n\n")
    return parse_stacks(diagram), parse_moves(moves)


assert parse_data(example) == (
    {1: ["Z", "N"], 2: ["M", "C", "D"], 3: ["P"]},
    [(2, 1), (1, 3), (1, 3), (1, 3), (2, 1), (2, 1), (1, 2)],
)


def move_boxes(start_diagram: Dict[int, List], moves: List[Tuple[int, int]]) -> Dict[int, List]:
    box_diagram = start_diagram
    for move in moves:
        box_diagram[move[1]].append(box_diagram[move[0]].pop())
    return box_diagram


assert move_boxes(*parse_data(example)) == {1: ["C"], 2: ["M"], 3: ["P", "D", "N", "Z"]}


def extract_tops(box_diagram: Dict[int, List]) -> str:
    tops = ""
    for key in box_diagram:
        tops = tops + box_diagram[key][-1]
    return tops


assert extract_tops(move_boxes(*parse_data(example))) == "CMZ"


def parse_multi_moves(moveset: str) -> List[Tuple[int, int, int]]:
    text_moves = [row.split() for row in moveset.split("\n")]
    simple_moves = []
    for row in text_moves:
        simple_moves.append((int(row[3]), int(row[5]), int(row[1])))
    return simple_moves


def parse_multi_data(problem_input: str) -> Tuple[Dict[int, List], List[Tuple[int, int, int]]]:
    diagram, moves = problem_input.split("\n\n")
    return parse_stacks(diagram), parse_multi_moves(moves)


assert parse_multi_data(example) == (
    {1: ["Z", "N"], 2: ["M", "C", "D"], 3: ["P"]},
    [(2, 1, 1), (1, 3, 3), (2, 1, 2), (1, 2, 1)],
)


def multi_move_boxes(start_diagram: Dict[int, List], moves: List[Tuple[int, int, int]]) -> Dict[int, List]:
    box_diagram = start_diagram
    for move in moves:
        box_diagram[move[1]].extend(box_diagram[move[0]][-move[2]:])  # fmt: skip
        del box_diagram[move[0]][-move[2]:]  # fmt: skip
    return box_diagram


assert multi_move_boxes(*parse_multi_data(example)) == {1: ["M"], 2: ["C"], 3: ["P", "Z", "N", "D"]}

assert extract_tops(multi_move_boxes(*parse_multi_data(example))) == "MCD"

with open("outputs/output05.txt", "w") as file:
    file.write(extract_tops(move_boxes(*parse_data(solutions.read_input("05")))))
    file.write("\n")
    file.write(extract_tops(multi_move_boxes(*parse_multi_data(solutions.read_input("05")))))
