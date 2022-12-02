import solutions


def single_round(round: str) -> int:
    split_round = round.split()
    throw_value = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}
    shape_score = throw_value[split_round[1]]
    outcome_score = ((throw_value[split_round[1]] - throw_value[split_round[0]] + 1) % 3) * 3
    return shape_score + outcome_score


def test_single_round():
    assert single_round("A Y") == 8
    assert single_round("B X") == 1
    assert single_round("C Z") == 6


def single_round_inferred(round: str) -> int:
    split_round = round.split()
    throw_value = {"A": 1, "B": 2, "C": 3, "X": 0, "Y": 3, "Z": 6}
    shape_score = ((throw_value[split_round[0]] + (throw_value[split_round[1]] // 3) - 2) % 3) + 1
    outcome_score = throw_value[split_round[1]]
    return shape_score + outcome_score


def test_single_round_inferred():
    assert single_round_inferred("A Y") == 4
    assert single_round_inferred("B X") == 1
    assert single_round_inferred("C Z") == 7
    assert single_round_inferred("A Z") == 8
    assert single_round_inferred("A X") == 3


if __name__ == "__main__":
    test_single_round()
    test_single_round_inferred()
    scores = [
        (single_round(item), single_round_inferred(item))
        for item in solutions.read_input("02").split("\n")
        if len(item) > 0
    ]
    pivoted_scores = list(zip(*scores))
    with open("outputs/output02.txt", "w") as file:
        file.writelines([str(sum(pivoted_scores[0])), "\n", str(sum(pivoted_scores[1]))])
    file.close()
