from typing import Set, Tuple

import solutions

example = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""


def gather_cubes(cube_collection: str) -> Set[Tuple[int, int, int]]:
    return {tuple(map(int, row.split(","))) for row in cube_collection.splitlines()}  # type: ignore


def shift_axis(cube: Tuple[int, int, int], axis: int, shift: int) -> Tuple[int, int, int]:
    return tuple([cube_side + (shift if i == axis else 0) for i, cube_side in enumerate(cube)])  # type: ignore


def shift_and_compare(cubes: Set[Tuple[int, int, int]]) -> int:
    uncovered_sides = 6 * len(cubes)
    for axis in range(3):
        uncovered_sides -= 2 * len(cubes.intersection({shift_axis(cube, axis, 1) for cube in cubes}))
    return uncovered_sides


assert shift_and_compare(gather_cubes(example)) == 64


def air_coords(cube_collection: str) -> Tuple[Set[Tuple[int, int, int]], int]:
    cubes = gather_cubes(cube_collection)
    all_coords = [cube[i] for cube in cubes for i in range(3)]
    box_range = range(min(all_coords) - 1, max(all_coords) + 1)
    air_cubes = {(i, j, k) for i in box_range for j in box_range for k in box_range if (i, j, k) not in cubes}
    return air_cubes, box_range.start


def interior_air(cube_collection: str) -> Set[Tuple[int, int, int]]:
    air_cubes, start_coord = air_coords(cube_collection)
    outside_cubes = set()
    working_cubes = {(start_coord, start_coord, start_coord)}
    while working_cubes:
        current_cube = working_cubes.pop()
        outside_cubes.add(current_cube)
        working_cubes.update(
            {
                shift_axis(current_cube, axis, shift)
                for axis in range(3)
                for shift in [-1, 1]
                if shift_axis(current_cube, axis, shift) in air_cubes
                and shift_axis(current_cube, axis, shift) not in outside_cubes
            }
        )
    return air_cubes.difference(outside_cubes)


def surface_excl_interior(cube_collection: str) -> int:
    return shift_and_compare(gather_cubes(cube_collection)) - shift_and_compare(interior_air(cube_collection))


assert surface_excl_interior(example) == 58


with open("outputs/output18.txt", "w") as file:
    daily_input = solutions.read_input("18")
    file.write(str(shift_and_compare(gather_cubes(daily_input))))
    file.write("\n")
    file.write(str(surface_excl_interior(daily_input)))
