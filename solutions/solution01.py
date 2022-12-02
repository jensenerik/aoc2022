from typing import List

import solutions


def break_up_counts(counts: str) -> List[List[int]]:
    broken_but_strings = [item.split("\n") for item in counts.split("\n\n")]
    return [[int(item) for item in inner_list if item] for inner_list in broken_but_strings]


def maximum_counts(broken_counts: List[List[int]]) -> List[int]:
    return sorted([sum(inner_list) for inner_list in broken_counts], reverse=True)


if __name__ == "__main__":
    output = maximum_counts(break_up_counts(solutions.read_input("01")))[0:3]
    with open("outputs/output01.txt", mode="w") as file:
        file.writelines([str(output[0]), "\n", str(sum(output))])
    file.close()
