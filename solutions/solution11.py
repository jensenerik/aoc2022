from functools import reduce
from typing import Callable, List, NamedTuple, Optional, Tuple

import solutions

example = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""


class MonkeyRuleset(NamedTuple):
    monkey_id: int
    operation: Callable
    test: Callable
    true_target: int
    false_target: int
    test_divisor: int


def extract_last_int(data: List[str], row_num: int):
    return int(data[row_num].split()[-1])


def parse_input(input: str) -> Tuple[List[List[int]], List[MonkeyRuleset]]:
    items = []
    rules: List[MonkeyRuleset] = []
    for indiv_monkey in input.split("\n\n"):
        monkey_data = indiv_monkey.splitlines()
        monkey_number = int(monkey_data[0].split()[1][:-1])
        items.append([int(item) for item in monkey_data[1][18:].split(", ")])
        rules.append(
            MonkeyRuleset(
                monkey_number,
                lambda old, md=monkey_data: eval(md[2][19:]),
                lambda x, md=monkey_data: (x % extract_last_int(md, 3)) == 0,
                extract_last_int(monkey_data, 4),
                extract_last_int(monkey_data, 5),
                extract_last_int(monkey_data, 3),
            )
        )
    assert [monkey_rules.monkey_id for monkey_rules in rules] == list(range(len(rules)))
    return items, rules


def monkey_do(
    starting_items: List[List[int]], monkey_rules: MonkeyRuleset, remainder: Optional[int] = None
) -> List[List[int]]:
    items = starting_items.copy()
    for item in items[monkey_rules.monkey_id]:
        worry_level = monkey_rules.operation(item)
        worry_level = worry_level % remainder if remainder else worry_level // 3
        target = monkey_rules.true_target if monkey_rules.test(worry_level) else monkey_rules.false_target
        items[target].append(worry_level)
    items[monkey_rules.monkey_id] = []
    return items


def round_of_monkeys(
    starting_items: List[List[int]], all_rules: List[MonkeyRuleset], starting_touches: List[int], extended: bool = False
) -> Tuple[List[List[int]], List[int]]:
    items = starting_items.copy()
    touches = starting_touches.copy()
    remainder = reduce(lambda x, y: x * y, [monkey.test_divisor for monkey in all_rules])
    for monkey in all_rules:
        touches[monkey.monkey_id] += len(items[monkey.monkey_id])
        items = monkey_do(items, monkey, remainder if extended else None)
    return items, touches


assert round_of_monkeys(*parse_input(example), [0] * 4) == (
    [[20, 23, 27, 26], [2080, 25, 167, 207, 401, 1046], [], []],
    [2, 4, 3, 5],
)


def monkey_business(input: str, rounds: int, extended: bool = False) -> int:
    items, rules = parse_input(input)
    touches = [0] * len(rules)
    for i in range(rounds):
        items, touches = round_of_monkeys(items, rules, touches, extended)
    return reduce(lambda x, y: x * y, sorted(touches, reverse=True)[:2])


assert monkey_business(example, 20) == 10605
assert monkey_business(example, 10000, True) == 2713310158


with open("outputs/output11.txt", "w") as file:
    input = solutions.read_input("11")
    file.write(str(monkey_business(input, 20)))
    file.write("\n")
    file.write(str(monkey_business(input, 10000, True)))
