"""Second part of the challenge"""
from pathlib import Path
from app.main import read_input_file


class CubeSet:
    _max_red = 12
    _max_blue = 14
    _max_green = 13

    def __init__(self, nb_blue: int, nb_red: int, nb_green: int):
        self.nb_blue = nb_blue
        self.nb_red = nb_red
        self.nb_green = nb_green

    def is_valid(self):
        return (
            self.nb_blue <= self._max_blue
            and self.nb_red <= self._max_red
            and self.nb_green <= self._max_green
        )

    @classmethod
    def from_text(cls, text: str):
        text = text.strip()
        colors = text.split(",")

        nb_red = 0
        nb_green = 0
        nb_blue = 0

        for color in colors:
            color = color.strip()
            nb_cube, color = color.split()

            if color == "red":
                nb_red = int(nb_cube)
            elif color == "green":
                nb_green = int(nb_cube)
            elif color == "blue":
                nb_blue = int(nb_cube)
            else:
                raise ValueError(f"Unknown color {color}")

        return cls(nb_blue, nb_red, nb_green)


class LineContent:
    def __init__(self, content_id: int, sets: CubeSet) -> None:
        self.content_id = content_id
        self.sets = sets

    def power(self):
        max_red = max(cube_set.nb_red for cube_set in self.sets)
        max_green = max(cube_set.nb_green for cube_set in self.sets)
        max_blue = max(cube_set.nb_blue for cube_set in self.sets)

        return max_red * max_green * max_blue


def sum_valid_id(lines: list[LineContent]):
    return sum(
        line.content_id
        for line in lines
        if all(cube_set.is_valid() for cube_set in line.sets)
    )


def sum_power(lines: list[LineContent]):
    return sum(line.power() for line in lines)


def parse_line(line: str) -> LineContent:
    line = line.strip().replace(r"\n", "")
    content_id, cube_sets = line.split(":")

    content_id = content_id.split(" ")[1]

    cube_sets = cube_sets.split(";")

    cube_sets = [CubeSet.from_text(cube_set) for cube_set in cube_sets]

    return LineContent(int(content_id), cube_sets)


if __name__ == "__main__":
    input_path = Path(__file__).parent / "input.txt"

    lines = read_input_file(input_path)

    parsed_lines = [parse_line(line) for line in lines]

    print(sum_valid_id(parsed_lines))

    print(sum_power(parsed_lines))
