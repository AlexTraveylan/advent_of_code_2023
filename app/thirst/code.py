from pathlib import Path
from app.main import read_input_file

NUMBERS = "0123456789"


class Star:
    def __init__(self, line: int, column: int) -> None:
        self.line = line
        self.column = column

    def __repr__(self) -> str:
        return f"Star({self.line}, {self.column})"


def stars_index(lines: list[str]) -> list[Star]:
    stars = []

    for line_index, line in enumerate(lines):
        for column_index, char in enumerate(line):
            if char == "*":
                stars.append(Star(line_index, column_index))

    return stars


class Number:
    def __init__(
        self, number: str, line: int, columns: int, adjacents: str = None
    ) -> None:
        self.number = number
        self.line = line
        self.columns = columns
        self.adjacents = adjacents

    def __repr__(self) -> str:
        return f"Number({self.number}, {self.line}, {self.columns}, {self.adjacents})"

    def cast_int(self) -> int:
        digits = [digit for digit in self.number if digit in NUMBERS]

        return int("".join(digits))

    def is_valid(self, lines: list[str]) -> bool:
        if not self.number.isnumeric():
            star = self.number.find("*")
            if star != -1:
                star = Constellation.find_star_by_line_column(
                    self.line, self.columns + star
                )
                Constellation.add_number_to_star(star, self)

            return True

        try:
            before = lines[self.line][self.columns - 1]

            if before == "*":
                star = Constellation.find_star_by_line_column(
                    self.line, self.columns - 1
                )
                Constellation.add_number_to_star(star, self)
        except:
            before = "."

        try:
            after = lines[self.line][self.columns + len(self.number)]

            if after == "*":
                star = Constellation.find_star_by_line_column(
                    self.line, self.columns + len(self.number)
                )
                Constellation.add_number_to_star(star, self)
        except:
            after = "."

        try:
            above = lines[self.line - 1][self.columns : self.columns + len(self.number)]

            if "*" in above:
                star = Constellation.find_star_by_line_column(
                    self.line - 1, self.columns + above.index("*")
                )
                Constellation.add_number_to_star(star, self)
        except:
            above = "."

        try:
            below = lines[self.line + 1][self.columns : self.columns + len(self.number)]

            if "*" in below:
                star = Constellation.find_star_by_line_column(
                    self.line + 1, self.columns + below.index("*")
                )
                Constellation.add_number_to_star(star, self)
        except:
            below = "."

        try:
            diag_top_left = lines[self.line - 1][self.columns - 1]

            if diag_top_left == "*":
                star = Constellation.find_star_by_line_column(
                    self.line - 1, self.columns - 1
                )
                Constellation.add_number_to_star(star, self)
        except:
            diag_top_left = "."

        try:
            diag_top_right = lines[self.line - 1][self.columns + len(self.number)]

            if diag_top_right == "*":
                star = Constellation.find_star_by_line_column(
                    self.line - 1, self.columns + len(self.number)
                )
                Constellation.add_number_to_star(star, self)
        except:
            diag_top_right = "."

        try:
            diag_bottom_left = lines[self.line + 1][self.columns - 1]

            if diag_bottom_left == "*":
                star = Constellation.find_star_by_line_column(
                    self.line + 1, self.columns - 1
                )
                Constellation.add_number_to_star(star, self)
        except:
            diag_bottom_left = "."

        try:
            diag_bottom_right = lines[self.line + 1][self.columns + len(self.number)]

            if diag_bottom_right == "*":
                star = Constellation.find_star_by_line_column(
                    self.line + 1, self.columns + len(self.number)
                )
                Constellation.add_number_to_star(star, self)
        except:
            diag_bottom_right = "."

        all_adjacents = [
            before,
            after,
            *above,
            *below,
            diag_top_left,
            diag_top_right,
            diag_bottom_left,
            diag_bottom_right,
        ]

        self.adjacents = all_adjacents

        if all(
            number == "." or number.isdigit() or number == "\n"
            for number in all_adjacents
        ):
            return False
        else:
            return True


class Constellation:
    _stars: dict[Star, list[Number]] = {}

    @classmethod
    def init(cls, stars: list[Star]) -> None:
        for star in stars:
            cls._stars[star] = []

    @classmethod
    def add_number_to_star(cls, star: Star, number: Number) -> None:
        if star not in cls._stars:
            cls._stars[star] = []

        cls._stars[star].append(number)

    @classmethod
    def find_star_by_line_column(cls, line: int, column: int) -> Star:
        for star in cls._stars:
            if star.line == line and star.column == column:
                return star


def find_special_separator(number: str) -> str:
    separator = ""
    for digit in number[1:-1]:
        if digit not in NUMBERS:
            separator += digit

    return None if separator == "" else separator


def parse_lines(stripped_lines: list[str]) -> list[Number]:
    numbers = []

    for index_line, line in enumerate(stripped_lines):
        decal_index_column = 0
        for index_column, element in enumerate(line):
            if any(number in element for number in NUMBERS):
                separator = find_special_separator(element)
                if separator:
                    element_1, element_2 = element.split(separator)
                    numbers.append(
                        Number(element_1, index_line, index_column + decal_index_column)
                    )
                    numbers.append(
                        Number(
                            element_2,
                            index_line,
                            index_column
                            + decal_index_column
                            + len(element_1)
                            + len(separator),
                        )
                    )
                else:
                    numbers.append(
                        Number(element, index_line, index_column + decal_index_column)
                    )

                decal_index_column += len(element)
            elif element != "":
                decal_index_column += 1

    return numbers


def print_sum(numbers: list[Number]) -> None:
    cast_int = [number.cast_int() for number in numbers]

    return sum(cast_int)


if __name__ == "__main__":
    input_path = Path(__file__).parent / "input.txt"

    lines = read_input_file(input_path)

    stars_index = stars_index(lines)

    Constellation.init(stars_index)

    stripped_lines = [line.strip().split(".") for line in lines]

    numbers = parse_lines(stripped_lines)

    valid_numbers = [number for number in numbers if number.is_valid(lines)]

    print(print_sum(valid_numbers))

    v2_sum = 0

    for star, numbers in Constellation._stars.items():
        if len(numbers) == 2:
            v2_sum += numbers[0].cast_int() * numbers[1].cast_int()

    print(v2_sum)
