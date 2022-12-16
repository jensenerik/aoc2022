from typing import Dict, List, Tuple

import solutions

example = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""


class Valve:
    name: str
    flow_rate: int
    tunnels: List[str]

    def __init__(self, valve_row: str):
        self.name = valve_row[6:8]
        self.flow_rate = int(valve_row.split(";")[0][valve_row.find("=") + 1 :])
        if valve_row.find("leads") >= 0:
            self.tunnels = [valve_row.split("valve ")[-1]]
        else:
            self.tunnels = valve_row.split("valves ")[-1].split(", ")


class ValveMap:
    valves: Dict[str, Valve]
    open_status: Dict[str, bool]
    time_step: int
    total_time: int
    total_flow: int
    current_location: str
    other_time_step: int
    other_location: str

    def __init__(
        self,
        valves: Dict[str, Valve],
        open_status: Dict[str, bool],
        time_step: int,
        total_time: int,
        total_flow: int,
        current_location: str,
        other_time_step: int,
        other_location: str,
    ):
        self.valves = valves
        self.open_status = open_status
        self.time_step = time_step
        self.total_time = total_time
        self.total_flow = total_flow
        self.current_location = current_location
        self.other_time_step = other_time_step
        self.other_location = other_location

    def __repr__(self):
        return str((self.time_step, self.total_flow, self.current_location))

    def open_valve(self, valve_name: str):
        self.open_status[valve_name] = True

    def potential_flow(self, valve_name: str) -> int:
        return 0 if self.open_status[valve_name] else self.valves[valve_name].flow_rate

    def apply_dijkstra(self) -> Dict[str, int]:
        output = {self.current_location: 0}
        path_length = 1
        new_nodes = [self.current_location]
        while new_nodes:
            new_tunnels = {
                tunnel: path_length
                for node in new_nodes
                for tunnel in self.valves[node].tunnels
                if tunnel not in output
            }
            output.update(new_tunnels)
            path_length += 1
            new_nodes = list(new_tunnels.keys())
        return output

    def scores(self) -> Dict[str, Tuple[int, int]]:
        valve_distances = self.apply_dijkstra()
        return {
            valve_name: (
                (self.potential_flow(valve_name) * (self.total_time - self.time_step - distance - 1)),
                distance + 1,
            )
            for valve_name, distance in valve_distances.items()
            if (self.total_time - self.time_step > distance + 1) and (self.potential_flow(valve_name) > 0)
        }


def valve_map(instructions: str, total_time: int) -> ValveMap:
    valves = {}
    for row in instructions.splitlines():
        valve = Valve(row)
        valves[valve.name] = valve
    return ValveMap(valves, {valve_name: False for valve_name in valves}, 0, total_time, 0, "AA", 0, "AA")


def create_step(valve_map: ValveMap, candidates: int) -> List[ValveMap]:
    scores = sorted(valve_map.scores().items(), key=lambda x: x[1], reverse=True)
    output = []
    for step in scores[0:candidates]:
        new_location = step[0]
        gain = step[1][0]
        distance = step[1][1]
        new_valve_map = ValveMap(
            valve_map.valves,
            valve_map.open_status | {new_location: True},
            valve_map.time_step + distance,
            valve_map.total_time,
            valve_map.total_flow + gain,
            new_location,
            valve_map.other_time_step,
            valve_map.other_location,
        )
        output.append(new_valve_map)
    return output


def iterate_steps(instructions: str, candidates: int, flip_mode: bool = False) -> int:
    endings: List[ValveMap] = []
    working_list = [valve_map(instructions, 26 if flip_mode else 30)]
    next_list: List[ValveMap] = []
    while working_list:
        for step in working_list:
            if flip_mode and (step.time_step > step.other_time_step):
                step.time_step, step.other_time_step = step.other_time_step, step.time_step
                step.current_location, step.other_location = step.other_location, step.current_location
            new_steps = create_step(step, candidates)
            if new_steps:
                next_list.extend(new_steps)
            else:
                endings.append(step)
        working_list = sorted(next_list, key=lambda valve: valve.total_flow // valve.total_time, reverse=True)[
            0 : candidates**2
        ]
        next_list = []
    return max(endings, key=lambda x: x.total_flow).total_flow


assert iterate_steps(example, 3) == 1651
assert iterate_steps(example, 3, True) == 1707

with open("outputs/output16.txt", "w") as file:
    daily_input = solutions.read_input("16")
    file.write(str(iterate_steps(daily_input, 13)))
    file.write("\n")
    file.write(str(iterate_steps(daily_input, 30, True)))
