from typing import Tuple

import solutions


def explicit_range(hyphenated_range: str) -> range:
    edges = hyphenated_range.split("-")
    return range(int(edges[0]), int(edges[1]) + 1)


def parse_pair(range_pair: str) -> Tuple[range, ...]:
    explicit_pair = tuple([explicit_range(item) for item in range_pair.split(",")])
    return explicit_pair


def test_parse_pair():
    assert parse_pair("2-4,6-8") == (range(2, 5), range(6, 9))
    assert parse_pair("6-6,4-6") == (range(6, 7), range(4, 7))


def range_containment(range_pair: str) -> bool:
    range_0, range_1 = parse_pair(range_pair)
    return (range_0.start - range_1.start) * (range_0.stop - range_1.stop) <= 0


def test_range_containment():
    assert not range_containment("2-4,6-8")
    assert not range_containment("2-3,4-5")
    assert not range_containment("5-7,7-9")
    assert range_containment("2-8,3-7")
    assert range_containment("6-6,4-6")
    assert not range_containment("2-6,4-8")
    assert range_containment("86-87,16-87")
    assert not range_containment("3-86,87-87")
    assert not range_containment("92-96,17-91")
    assert range_containment("54-85,54-87")


def process_range_pairs(range_pairs: str) -> int:
    return sum([range_containment(row) for row in range_pairs.split("\n")])


def range_overlap(range_pair: str) -> bool:
    range_0, range_1 = parse_pair(range_pair)
    return (range_0.start - range_1.stop + 1) * (range_0.stop - range_1.start - 1) <= 0


def process_overlap_pairs(range_pairs: str) -> int:
    return sum([range_overlap(row) for row in range_pairs.split("\n")])


def test_range_overlap():
    assert not range_overlap("2-4,6-8")
    assert not range_overlap("2-3,4-5")
    assert range_overlap("5-7,7-9")
    assert range_overlap("2-8,3-7")
    assert range_overlap("6-6,4-6")
    assert range_overlap("2-6,4-8")
    assert range_overlap("86-87,16-87")
    assert not range_overlap("3-86,87-87")
    assert not range_overlap("92-96,17-91")
    assert range_overlap("54-85,54-87")


if __name__ == "__main__":
    test_parse_pair()
    test_range_containment()
    test_range_overlap()
    with open("outputs/output04.txt", "w") as file:
        file.write(str(process_range_pairs(solutions.read_input("04"))))
        file.write("\n")
        file.write(str(process_overlap_pairs(solutions.read_input("04"))))
