__version__ = "0.1.0"


def read_input(day: str) -> str:
    with open(f"inputs/input{day}.txt") as file:
        return file.read().strip("\n")
