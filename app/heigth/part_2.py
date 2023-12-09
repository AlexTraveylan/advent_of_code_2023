import time
from app.template import get_example, get_input, submit, ints
import numpy as np


class Parser:
    def __init__(
        self,
        left_right_instructions: str,
        possible_directions: dict[str, tuple[str, str]],
    ):
        self.left_right_instructions = left_right_instructions
        self.possible_directions = possible_directions

    @classmethod
    def from_lines(cls, lines: str):
        left_right_instructions = lines[0]
        left_right_in_number = np.array(
            [0 if x == "L" else 1 for x in left_right_instructions]
        )

        possible_directions = {}
        for line in lines[2:]:
            key, values = line.split(" = ")
            left, right = values.split(", ")
            possible_directions[key] = (left[1:], right[:-1])

        return cls(left_right_in_number, possible_directions)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.left_right_instructions}, {self.possible_directions})"


def end_condition(x) -> bool:
    is_end = all(actual_step[-1] == "Z" for actual_step in x)

    return is_end


def execute_instructions(parser: Parser) -> int:
    begins = [key for key in parser.possible_directions if key[-1] == "A"]

    actual_steps = begins.copy()

    nb_steps = 0

    while end_condition(actual_steps) is False:
        for instruction in parser.left_right_instructions:

            def get_next_step(x) -> str:
                direction = parser.possible_directions[x][instruction]
                return direction

            actual_steps = [get_next_step(x) for x in actual_steps]

            nb_steps += 1

    return nb_steps


def ppcm(*n):
    """Calcul du 'Plus Petit Commun Multiple' de n (>=2) valeurs entières (Euclide)"""

    def _pgcd(a, b):
        while b:
            a, b = b, a % b
        return a

    p = abs(n[0] * n[1]) // _pgcd(n[0], n[1])
    for x in n[2:]:
        p = abs(p * x) // _pgcd(p, x)
    return p


def length_cycle(start: str, parser: Parser) -> int:
    saved_way = [start]
    actual_step = start
    while True:
        for instruction in parser.left_right_instructions:
            actual_step = parser.possible_directions[actual_step][instruction]

        if actual_step in saved_way and actual_step[-1] == "Z":
            cycle = len(saved_way) - saved_way.index(actual_step)
            decal = len(saved_way) - cycle

            return decal, cycle

        saved_way.append(actual_step)


if __name__ == "__main__":
    DAY = 8
    PART = 2
    exemple_or_real = int(input("Exemple (0) ou Réel (1) ? "))

    if exemple_or_real == 0:
        s = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""
    else:
        s = get_input(DAY).strip()

    begin_time = time.perf_counter()

    parser = Parser.from_lines(s.splitlines())

    begins = [key for key in parser.possible_directions if key[-1] == "A"]

    cycles = [length_cycle(begin, parser) for begin in begins]

    ans = ppcm(*[cycle[1] for cycle in cycles])

    import math

    print(math.prod([cycle[1] for cycle in cycles]))

    # steps = execute_instructions(parser)

    # Your code here
    # ans = steps
    ans = ans * len(parser.left_right_instructions)

    # fin du code
    end_time = time.perf_counter()
    print(f"Temps d'exécution : {end_time - begin_time:.2f} secondes")
    if exemple_or_real == 1:
        submit(DAY, PART, ans)
    else:
        print(ans)
