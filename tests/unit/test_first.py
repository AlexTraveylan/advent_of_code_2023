from app.first.code import sum_calibration_values, sum_calibration_values_v2
import pytest


@pytest.mark.parametrize(
    "input, expected",
    [
        (["two1nine"], 29),
        (["eightwothree"], 83),
        (["abcone2threexyz"], 13),
        (["xtwone3four"], 24),
        (["4nineeightseven2"], 42),
        (["zoneight234"], 14),
        (["7pqrstsixteen"], 76),
        (["one1two2three3four4five5six6seven7eight8nine9"], 19),
        (["oneoneoneoneoneonetwoone"], 11)
    ],
)
def test_01_12_2023_v2(input, expected):
    assert sum_calibration_values_v2(input) == expected


def test_v2_sum():
    lines = [
        "two1nine",
        "eightwothree",
        "abcone2threexyz",
        "xtwone3four",
        "4nineeightseven2",
        "zoneight234",
        "7pqrstsixteen",
    ]

    assert sum_calibration_values_v2(lines) == 281


@pytest.mark.parametrize(
    "input, expected",
    [
        (["1abc2"], 12),
        (["pqr3stu8vwx"], 38),
        (["a1b2c3d4e5f"], 15),
        (["treb7uchet"], 77),
    ],
)
def test_01_12_2023_v1(input, expected):
    assert sum_calibration_values(input) == expected


def test_v1_sum():
    lines = ["1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet"]

    assert sum_calibration_values(lines) == 142
