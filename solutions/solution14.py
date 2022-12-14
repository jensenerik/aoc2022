from typing import Dict, List, Tuple

import solutions

example = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


def coord_line(coord_1: Tuple[int, int], coord_2: Tuple[int, int]) -> List[Tuple[int, int]]:
    x_coords = (coord_1[0], coord_2[0])
    y_coords = (coord_1[1], coord_2[1])
    output = []
    for i in range(min(x_coords), max(x_coords) + 1):
        for j in range(min(y_coords), max(y_coords) + 1):
            output.append((i, j))
    return output


def rock_map(paths: str) -> Dict[Tuple[int, int], bool]:
    output: Dict[Tuple[int, int], bool] = {}
    for row in paths.splitlines():
        corners = [tuple(map(int, coord.split(","))) for coord in row.split(" -> ")]
        last_corner = corners[0]
        for corner_coord in corners[1:]:
            output.update({path_coord: True for path_coord in coord_line(last_corner, corner_coord)})
            last_corner = corner_coord
    return output


def sand_drop(
    solid_coords: Dict[Tuple[int, int], bool], start_coord: Tuple[int, int], fixed_depth: int = 100
) -> Tuple[int, int]:
    depth = 0
    while depth < fixed_depth:
        straight_down = (start_coord[0], start_coord[1] + depth)
        diag_left = (start_coord[0] - 1, start_coord[1] + depth)
        diag_right = (start_coord[0] + 1, start_coord[1] + depth)
        if straight_down in solid_coords:
            if diag_left in solid_coords:
                if diag_right in solid_coords:
                    return (start_coord[0], start_coord[1] + depth - 1)
                else:
                    return sand_drop(solid_coords, diag_right, fixed_depth)
            else:
                return sand_drop(solid_coords, diag_left, fixed_depth)
        else:
            depth += 1


def count_sand(solid_coords: Dict[Tuple[int, int], bool], start_coord: Tuple[int, int], fixed_depth: int = 100):
    sand_count = 0
    solid_map = solid_coords.copy()
    new_one = True
    while new_one and (new_one != start_coord):
        new_one = sand_drop(solid_map, start_coord, fixed_depth)
        solid_map.update({new_one: True})
        sand_count += 1
    return sand_count - 1


assert count_sand(rock_map(example), (500, 0), 100) == 24


def count_w_floor(paths: str, start_coord: Tuple[int, int], floor_depth: int = 2):
    floor_extension = 2000
    solid_map = rock_map(paths)
    lowest_rock = max([coord[1] for coord in solid_map])
    rock_x_coord = [coord[0] for coord in solid_map]
    min_x, max_x = (min(rock_x_coord), max(rock_x_coord))
    solid_map.update(
        {
            (floor_x, lowest_rock + floor_depth): True
            for floor_x in range(min_x - floor_extension, max_x + floor_extension)
        }
    )
    return count_sand(solid_map, start_coord) + 1


assert count_w_floor(example, (500, 0), 2) == 93

with open("outputs/output14.txt", "w") as file:
    daily_input = solutions.read_input("14")
    file.write(str(count_sand(rock_map(daily_input), (500, 0), 100)))
    file.write("\n")
    file.write(str(count_w_floor(daily_input, (500, 0), 2)))
