from typing import Dict, List, Optional, Tuple

import solutions

example = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""


def do_operation(operand: int, operation: str, operand_2: int) -> Optional[int]:
    if operation == "+":
        return operand + operand_2
    elif operation == "-":
        return operand - operand_2
    elif operation == "*":
        return operand * operand_2
    elif operation == "/":
        if operand % operand_2 == 0:
            return operand // operand_2
    return None


def parse_monkeys(monkey_rules: str) -> Tuple[Dict[str, int], Dict[str, List[str]]]:
    operators = {}
    numbers = {}
    for row in monkey_rules.splitlines():
        split_row = row.split()
        if len(split_row) == 2:
            numbers[split_row[0][:-1]] = int(split_row[1])
        else:
            operators[split_row[0][:-1]] = split_row[1:]
    return numbers, operators


def forward_monkeys(numbers: Dict[str, int], operators: Dict[str, List[str]]) -> Optional[int]:
    while "root" not in numbers:
        for monkey, operation in operators.items():
            if operation[0] in numbers and operation[2] in numbers:
                answer = do_operation(numbers[operation[0]], operation[1], numbers[operation[2]])
                if answer:
                    numbers[monkey] = answer
                else:
                    return None
    return numbers["root"]


assert forward_monkeys(*parse_monkeys(example)) == 152


def reverse_monkeys(monkey_rules: str) -> List[Tuple[int, int]]:
    numbers, operators = parse_monkeys(monkey_rules)
    near_b = 61271425704935
    near_m = 17
    step = 3705 - 345
    start = near_b // near_m - (near_b // near_m % step) + 345
    operators["root"][1] = "-"
    answers = []
    for i in range(start, start + step * 20, step):
        answer = forward_monkeys(numbers | {"humn": i}, operators)
        if answer:
            answers.append((i, answer))
    return answers


with open("outputs/output21.txt", "w") as file:
    daily_input = solutions.read_input("21")
    file.write(str(forward_monkeys(*parse_monkeys(daily_input))))
    file.write("\n")
    test_cases = reverse_monkeys(daily_input)
    case_0 = test_cases[0]
    case_1 = test_cases[1]
    file.write(str(-case_0[1] * (case_0[0] - case_1[0]) / (case_0[1] - case_1[1]) + case_0[0]))
