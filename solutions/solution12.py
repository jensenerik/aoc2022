from typing import Dict, List, NamedTuple, Tuple

import solutions

example = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


class graphData(NamedTuple):
    start: Tuple[int, int]
    end: Tuple[int, int]
    adjacency: Dict[Tuple[int, int], List[Tuple[int, int]]]
    extra_lows: List[Tuple[int, int]]


def create_graph(diagram: str) -> graphData:
    graph_list_format = diagram.splitlines()
    letter_translation = {chr(x): x - 97 for x in (range(97, 123))}
    letter_translation["S"] = 0
    letter_translation["E"] = 25
    adjacency: Dict[Tuple[int, int], List[Tuple[int, int]]] = {
        (i, j): [] for i in range(len(graph_list_format)) for j in range(len(graph_list_format[0]))
    }
    extra_lows = []
    for i, row in enumerate(graph_list_format):
        for j, item in enumerate(row):
            if item == "S":
                start = (i, j)
            elif item == "E":
                end = (i, j)
            if letter_translation[item] == 0:
                extra_lows.append((i, j))
            for coord in [(i, j + y) for y in [-1, +1]] + [(i + x, j) for x in [-1, +1]]:
                if (coord in adjacency) and (
                    letter_translation[graph_list_format[coord[0]][coord[1]]] <= letter_translation[item] + 1
                ):
                    adjacency[(i, j)].append(coord)
    return graphData(start, end, adjacency, extra_lows)


def apply_dijkstra(graph: graphData, quit_number: int, single_end: bool = True) -> int:
    total_nodes = len(graph.adjacency)
    path_lengths = {k: total_nodes for k in graph.adjacency}
    path_lengths[graph.start] = 0
    rounds = 0
    while rounds < quit_number and (
        (path_lengths[graph.end] == total_nodes)
        if single_end
        else min([path_lengths[end] for end in graph.extra_lows]) == total_nodes
    ):
        min_length = min([length for length in path_lengths.values() if length >= 0])
        min_nodes = [k for k in path_lengths if path_lengths[k] == min_length]
        for node in min_nodes:
            for adj_node in graph.adjacency[node]:
                if path_lengths[adj_node] > min_length:
                    path_lengths[adj_node] = min_length + 1
        path_lengths[node] = -1  # remove node from algorithm without key errors
        rounds += 1
    return path_lengths[graph.end] if single_end else min([path_lengths[end] for end in graph.extra_lows])


assert apply_dijkstra(create_graph(example), 500) == 31


def reverse_adjacency(graph: graphData) -> graphData:
    adjacency: Dict[Tuple[int, int], List[Tuple[int, int]]] = {k: [] for k in graph.adjacency}
    for k, v in graph.adjacency.items():
        for coord in v:
            adjacency[coord].append(k)
    return graphData(graph.end, graph.start, adjacency, graph.extra_lows)


apply_dijkstra(reverse_adjacency(create_graph(example)), 500, False) == 29

with open("outputs/output12.txt", "w") as file:
    input = solutions.read_input("12")
    file.write(str(apply_dijkstra(create_graph(input), 10000)))
    file.write("\n")
    file.write(str(apply_dijkstra(reverse_adjacency(create_graph(input)), 10000, False)))
