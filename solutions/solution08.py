from functools import reduce
from typing import Dict, List, Set, Tuple

import solutions

example = """30373
25512
65332
33549
35390"""


def horizontal_views(diagram: str) -> List[Tuple[int, ...]]:
    return [tuple([int(item) for item in list(row)]) for row in diagram.split("\n")]


def vertical_views(diagram: str) -> List[Tuple[int, ...]]:
    return list(zip(*horizontal_views(diagram)))


def find_visible(view: Tuple[int, ...], tracker: int) -> Set[Tuple[int, int]]:
    visible = set()
    for i, height in enumerate(view):
        if (height > max(view[:i], default=-1)) or (height > max(view[i + 1:], default=-1)):  # fmt: skip
            visible.add((i, tracker))
    return visible


def all_visible(diagram: str) -> Set[Tuple[int, ...]]:
    visible = set()
    horiz = horizontal_views(diagram)
    vert = vertical_views(diagram)
    for i, view in enumerate(horiz):
        visible.update({tuple(reversed(item)) for item in find_visible(view, i)})
    for i, view in enumerate(vert):
        visible.update(find_visible(view, i))
    return visible


assert len(all_visible(example)) == 21


def interior_visible(view: Tuple[int, ...], tracker: int) -> Dict[Tuple[int, int], List[int]]:
    int_visible: Dict[Tuple[int, int], List[int]] = dict()
    for i, height in enumerate(view):
        two_sided_visible = []
        blocking = [(item >= height) for item in view]
        left = list(reversed(blocking[:i]))
        right = blocking[i + 1:]  # fmt: skip
        for direction in [left, right]:
            if True in direction:
                two_sided_visible.append(direction.index(True) + 1)
            else:
                two_sided_visible.append(len(direction))
        int_visible[(i, tracker)] = two_sided_visible
    return int_visible


def all_interior_visible(diagram: str) -> Dict[Tuple[int, ...], List[int]]:
    visible = dict()
    horiz = horizontal_views(diagram)
    vert = vertical_views(diagram)
    for i, view in enumerate(horiz):
        visible.update({tuple(reversed(k)): v for k, v in interior_visible(view, i).items()})
    for i, view in enumerate(vert):
        visible.update({k: visible[k] + v for k, v in interior_visible(view, i).items()})
    return visible


def find_max_visible(diagram: str):
    return max([reduce(lambda x, y: x * y, v) for _, v in all_interior_visible(diagram).items()])


assert find_max_visible(example) == 8

with open("outputs/output08.txt", "w") as file:
    input = solutions.read_input("08")
    file.write(str(len(all_visible(input))))
    file.write("\n")
    file.write(str(find_max_visible(input)))
