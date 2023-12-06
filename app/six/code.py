from functools import reduce
from pathlib import Path

from app.main import read_input_file


class Parser:
    def __init__(self, lines: list[str]):
        self.lines = lines

    def parse_times(self):
        times_str = self.lines[0].split(":")[1].strip().split()

        return [int(time) for time in times_str]

    def parse_distances(self):
        distances_str = self.lines[1].split(":")[1].strip().split()

        return [int(distance) for distance in distances_str]


def possibilities(time, distance):
    olding_button_possibilities = range(time)

    wins_counter = 0

    for possibility in olding_button_possibilities:
        time_left = time - possibility
        speed = possibility

        distance_possible = speed * time_left
        if distance_possible > distance:
            wins_counter += 1

    return wins_counter


def result(times, distances):
    wins_counter = 1

    for time, distance in zip(times, distances):
        wins_counter *= possibilities(time, distance)

    return wins_counter


if __name__ == "__main__":
    input_path = Path(__file__).parent / "input.txt"

    lines = read_input_file(input_path)

    parser = Parser(lines)
    times = parser.parse_times()

    print(times)

    distances = parser.parse_distances()

    print(distances)

    wins = possibilities(times[0], distances[0])
    print(wins)

    print(result(times, distances))

    real_time = int(reduce(lambda curr, acc: curr + str(acc), times, ""))
    print(real_time)
    real_distance = int(reduce(lambda curr, acc: curr + str(acc), distances, ""))
    print(real_distance)

    print(possibilities(real_time, real_distance))
