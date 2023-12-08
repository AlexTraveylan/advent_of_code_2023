import time
from app.template import get_example, get_input, submit, ints


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

        possible_directions = {}
        for line in lines[2:]:
            key, values = line.split(" = ")
            left, right = values.split(", ")
            possible_directions[key] = (left[1:], right[:-1])

        return cls(left_right_instructions, possible_directions)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.left_right_instructions}, {self.possible_directions})"


def execute_instructions(parser: Parser) -> int:
    begins = [key for key in parser.possible_directions if key[-1] == "A"]
    actual_steps = begins.copy()

    def end_condition(x) -> bool:
        return all(actual_step.endswith("Z") for actual_step in x)

    nb_steps = 0

    while end_condition(actual_steps) is False:
        for instruction in parser.left_right_instructions:
            for index, actual_step in enumerate(actual_steps):
                if instruction == "L":
                    actual_steps[index] = parser.possible_directions[actual_step][0]
                elif instruction == "R":
                    actual_steps[index] = parser.possible_directions[actual_step][1]

            nb_steps += 1

    return nb_steps


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
    nb_steps = execute_instructions(parser)

    # Your code here
    ans = nb_steps

    # fin du code
    end_time = time.perf_counter()
    print(f"Temps d'exécution : {end_time - begin_time:.2f} secondes")
    if exemple_or_real == 1:
        submit(DAY, PART, ans)
    else:
        print(ans)
