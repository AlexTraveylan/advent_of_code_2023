from pathlib import Path

from app.main import read_input_file


def sum_calibration_values(input_lines):
    sum_values = 0
    for line in input_lines:
        digits = [char for char in line if char.isdigit()]
        if digits:
            first_digit = digits[0]
            last_digit = digits[-1]
            calibration_value = int(first_digit + last_digit)
            sum_values += calibration_value
    return sum_values


DIGITS_DICTIONNARY = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
}


def find_first_digit(word):
    index = -1
    lower_index = 100000000
    lower_digit = None

    for digit in DIGITS_DICTIONNARY:
        index = word.find(digit)
        if index != -1:
            if index < lower_index:
                lower_index = index
                lower_digit = digit

    return DIGITS_DICTIONNARY[lower_digit]


def find_last_digit(word):
    index = -1
    higher_index = -1
    higher_digit = None

    for digit in DIGITS_DICTIONNARY:
        index = word.rfind(digit)
        if index != -1:
            if index > higher_index:
                higher_index = index
                higher_digit = digit

    return DIGITS_DICTIONNARY[higher_digit]


def sum_calibration_values_v2(input_lines):
    sum_values = 0

    for line in input_lines:
        first_digit = find_first_digit(line)
        last_digit = find_last_digit(line)
        calibration_value = int(first_digit + last_digit)
        sum_values += calibration_value

    return sum_values


if __name__ == "__main__":
    input_path = Path(__file__).parent / "input.txt"

    lines = read_input_file(input_path)

    print(sum_calibration_values(lines))

    print(sum_calibration_values_v2(lines))
