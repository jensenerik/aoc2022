from typing import List

import solutions


def char_values(letter_sequence: str) -> List[int]:
    return [(value - 96) % 58 for value in letter_sequence.encode()]


def test_char_values():
    assert char_values("abcxyzABCXYZ") == [1, 2, 3, 24, 25, 26, 27, 28, 29, 50, 51, 52]


def common_between_halves(encoded_list: List[int]) -> int:
    half_length = len(encoded_list) // 2
    return set(encoded_list[0:half_length]).intersection(encoded_list[half_length:]).pop()


def test_common_between_halves():
    assert common_between_halves(char_values("vJrwpWtwJgWrhcsFMMfFFhFp")) == char_values("p")[0]
    assert common_between_halves(char_values("jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL")) == char_values("L")[0]


def process_common(file_values: List[List[int]]) -> int:
    return sum([common_between_halves(item) for item in file_values])


def process_badges(file_values: List[List[int]]) -> int:
    badges = []
    for triplet_number in range(len(file_values) // 3):
        badges.append(
            set(file_values[triplet_number * 3])
            .intersection(file_values[(triplet_number * 3) + 1])
            .intersection(file_values[(triplet_number * 3) + 2])
            .pop()
        )
    return sum(badges)


if __name__ == "__main__":
    test_char_values()
    test_common_between_halves()
    file_values: List[List[int]] = [
        char_values(item) for item in solutions.read_input("03").split("\n") if len(item) > 0
    ]
    with open("outputs/output03.txt", "w") as file:
        file.write(str(process_common(file_values)))
        file.write("\n")
        file.write(str(process_badges(file_values)))
    file.close()
