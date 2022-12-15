from typing import List, Optional, Set, Tuple

import solutions

example = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""


class SensorData:
    sensor_location: Tuple[int, int]
    nearest_beacon: Tuple[int, int]
    beacon_distance: int

    def __init__(self, sensor_row: str):
        row_chunks = sensor_row.split("=")
        colon_location = row_chunks[2].find(":")
        self.sensor_location = (int(row_chunks[1][:-3]), int(row_chunks[2][:colon_location]))
        self.nearest_beacon = (int(row_chunks[3][:-3]), int(row_chunks[4]))
        self.beacon_distance = abs(self.sensor_location[0] - self.nearest_beacon[0]) + abs(
            self.sensor_location[1] - self.nearest_beacon[1]
        )

    def disallowed_locations(self, row_num: int) -> List[Tuple[int, int]]:
        # disallowed includes all sensors and beacons
        disallowed = []
        vertical = row_num
        horizontal_bound = self.beacon_distance - abs(self.sensor_location[1] - vertical)
        for horizontal in range(
            self.sensor_location[0] - horizontal_bound,
            self.sensor_location[0] + horizontal_bound + 1,
        ):
            disallowed.append((horizontal, vertical))
        return disallowed


def acquire_disallowed(sensors: str, row_num: int) -> Set[Tuple[int, int]]:
    objects = set()
    disallowed = set()
    for row in sensors.splitlines():
        sensor_data = SensorData(row)
        objects.update([sensor_data.sensor_location, sensor_data.nearest_beacon])
        disallowed.update(sensor_data.disallowed_locations(row_num))
    return disallowed.difference(objects)


assert len(acquire_disallowed(example, 10)) == 26


def calculate_freq(coord: Tuple[int, int]) -> int:
    return (coord[0] * 4000000) + coord[1]


def heat_level(sensors: List[SensorData], coord: Tuple[int, int], boundaries: Tuple[int, int]) -> int:
    for i in range(2):
        if not ((coord[i] >= boundaries[0]) and (coord[i] <= boundaries[1])):
            return 1_000_000_000
    heat_levels = [
        sensor.beacon_distance
        - abs(sensor.sensor_location[0] - coord[0])
        - abs(sensor.sensor_location[1] - coord[1])
        + 1
        for sensor in sensors
    ]
    return sum([(heat if heat >= 0 else 0) for heat in heat_levels])


def gradient_descent(
    sensors: List[SensorData], starting_coord: Tuple[int, int], boundaries: Tuple[int, int]
) -> Optional[Tuple[int, int]]:
    def gd_step(
        sensor_data: List[SensorData], coord: Tuple[int, int], boundaries: Tuple[int, int]
    ) -> Optional[Tuple[int, int]]:
        base_heat = heat_level(sensor_data, coord, boundaries)
        if base_heat == 0:
            return coord
        else:
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            neighbors = [(coord[0] + direction[0], coord[1] + direction[1]) for direction in directions]
            neighbor_heat = [heat_level(sensor_data, neighbor, boundaries) for neighbor in neighbors]
            if min(neighbor_heat) >= base_heat:
                return None
            else:
                return neighbors[neighbor_heat.index(min(neighbor_heat))]

    current_coord = starting_coord
    while current_coord:
        next_coord = gd_step(sensors, current_coord, boundaries)
        if next_coord:
            if next_coord == current_coord:
                return current_coord
            else:
                current_coord = next_coord
        else:
            return None

    return current_coord


def identify_candidates(sensors: List[SensorData], boundaries: Tuple[int, int]) -> List[Tuple[int, int]]:
    boundary_length = boundaries[1] - boundaries[0]
    boundary_range = range(boundaries[0], boundaries[1] + 1, boundary_length // 10)
    grid = [(i, j) for i in boundary_range for j in boundary_range]
    grid.sort(key=lambda coord: heat_level(sensors, coord, boundaries))
    return grid[:10]


def candidate_grad_descent(sensors: str, boundaries: Tuple[int, int]) -> Optional[Tuple[int, int]]:
    sensor_data = [SensorData(row) for row in sensors.splitlines()]
    candidates = identify_candidates(sensor_data, boundaries)

    for candidate in candidates:
        gd_result = gradient_descent(sensor_data, candidate, boundaries)
        if gd_result:
            return gd_result
    return None


with open("outputs/output15.txt", "w") as file:
    daily_input = solutions.read_input("15")
    file.write(str(len(acquire_disallowed(daily_input, 2000000))))
    file.write("\n")
    missing_point = candidate_grad_descent(daily_input, (0, 4000000))
    if missing_point:
        file.write(str(calculate_freq(missing_point)))
