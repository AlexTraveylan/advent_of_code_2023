from functools import reduce
from app.six.code import Parser, possibilities, result


def test_six():
    exemple = """Time:      7  15   30\nDistance:  9  40  200\n"""
    parser_exemple = Parser(exemple.splitlines())

    times = parser_exemple.parse_times()
    assert times == [7, 15, 30]
    distances = parser_exemple.parse_distances()
    assert distances == [9, 40, 200]

    first_race_wins = 4

    assert possibilities(times[0], distances[0]) == 4

    assert result(times, distances) == 288

    real_time = int(reduce(lambda curr, acc: curr + str(acc), times, ""))
    real_distance = int(reduce(lambda curr, acc: curr + str(acc), distances, ""))

    assert possibilities(real_time, real_distance) == 71503
