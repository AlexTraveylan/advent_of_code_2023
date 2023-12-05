from pathlib import Path
import numpy as np
from numba import jit
from app.main import read_input_file

Seeds = list[int]


class ConvertLine:
    def __init__(
        self, destination_range_start: int, source_range_start: int, range_length: int
    ) -> None:
        self.destination_range_start = destination_range_start
        self.source_range_start = source_range_start
        self.range_length = range_length

        self.max_range = source_range_start + range_length - 1

        self.convert_step = destination_range_start - source_range_start

    @classmethod
    def from_line(cls, line: str):
        destination_range_start, source_range_start, range_length = line.split()
        return cls(
            int(destination_range_start), int(source_range_start), int(range_length)
        )

    def get(self, source_value: int) -> int:
        diff = source_value - self.source_range_start

        if self.source_range_start <= source_value <= self.max_range:
            return self.destination_range_start + diff
        else:
            return source_value

    def sure_get(self, source_value: int) -> int:
        return source_value + self.convert_step


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

    def get(self, source_value: int) -> int:
        for convertisseur in self.convertisseurs:
            if (
                convertisseur.source_range_start
                <= source_value
                <= convertisseur.max_range
            ):
                return convertisseur.sure_get(source_value)

        return source_value

    def numba_get(self, source_value: int) -> int:
        result = source_value
        for convertisseur in self.convertisseurs:
            convert_line_get(
                convertisseur.destination_range_start,
                convertisseur.source_range_start,
                convertisseur.range_length,
                result,
            )

        return result


class Almanac:
    def __init__(self, seeds: Seeds, convert_maps: list[ConvertMap]) -> None:
        self.seeds = seeds
        self.convert_maps = convert_maps

    @classmethod
    def from_lines(cls, lines: list[str]):
        seeds = [int(seed) for seed in lines[0].split(": ")[1].split()]

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


def seed_to_location(seed: int, almanac: Almanac) -> int:
    result = seed

    for convert_map in almanac.convert_maps:
        result = convert_map.get(result)

    return result


@jit(nopython=True)
def convert_line_get(
    destination_range_start: int,
    source_range_start: int,
    range_length: int,
    source_value: int,
) -> int:
    max_range = source_range_start + range_length - 1
    diff = source_value - source_range_start
    convert_step = destination_range_start - source_range_start

    if source_range_start <= source_value <= max_range:
        return destination_range_start + diff
    else:
        return source_value


if __name__ == "__main__":
    input_path = Path(__file__).parent / "input.txt"

    lines = read_input_file(input_path)
    lines_without_backslash_n = [line.replace("\n", "") for line in lines]

    almac = Almanac.from_lines(lines_without_backslash_n)

    mininum_location = min(seed_to_location(seed, almac) for seed in almac.seeds)

    print(mininum_location)

    reals_seeds = []
    seeds_starts = [seed for index, seed in enumerate(almac.seeds) if index % 2 == 0]
    ranges = [range for index, range in enumerate(almac.seeds) if index % 2 == 1]

    print("nombre de graines : ", sum(rang for rang in ranges))

    # minumums = []
    # for index, (seed_start, rang) in enumerate(zip(seeds_starts, ranges)):
    #     serie = [seed_start + i for i in range(rang // 100)]
    #     min_serie = min(seed_to_location(seed, almac) for seed in serie)

    #     minumums.append(min_serie)
    #     print(f"min_serie {index} :", min_serie)

    # print("minumum : ", min(minumums))
