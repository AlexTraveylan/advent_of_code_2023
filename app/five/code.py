from pathlib import Path
from app.main import read_input_file

Seeds = list[int]


class ConvertLine:
    def __init__(
        self, destination_range_start: int, source_range_start: int, range_length: int
    ) -> None:
        self.destination_range_start = destination_range_start
        self.source_range_start = source_range_start
        self.range_length = range_length

    @classmethod
    def from_line(cls, line: str):
        destination_range_start, source_range_start, range_length = line.split()
        return cls(
            int(destination_range_start), int(source_range_start), int(range_length)
        )


class ConvertMap:
    def __init__(self, title: str, convertisseurs: list[ConvertLine]) -> None:
        self.title = title
        self.convertisseurs = convertisseurs

    @classmethod
    def from_lines(cls, lines: list[str]):
        title = lines[0][:-1]
        convertisseurs = [ConvertLine.from_line(line) for line in lines[1:]]

        return cls(title, convertisseurs)

    @property
    def convert_role(self):
        source, destination = self.title.split()[0].split("-to-")
        return source, destination


class Almanac:
    def __init__(self, seeds: Seeds, convert_maps: list[ConvertMap]) -> None:
        self.seeds = seeds
        self.convert_maps = convert_maps

    @classmethod
    def from_lines(cls, lines: list[str]):
        seeds = [int(seed) for seed in lines[0].split(": ")[1].split()]

        start_condition = lambda line: line[:5].isalpha()
        end_condition = lambda line: line == ""

        convert_maps = []
        block = []
        for line in lines[2:]:
            if end_condition(line):
                convert_maps.append(ConvertMap.from_lines(block))
                block = []
            else:
                block.append(line)

        if len(block) > 0:
            convert_maps.append(ConvertMap.from_lines(block))

        return cls(seeds, convert_maps)


if __name__ == "__main__":
    input_path = Path(__file__).parent / "input.txt"

    lines = read_input_file(input_path)
