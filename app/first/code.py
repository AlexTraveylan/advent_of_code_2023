from pathlib import Path
import re


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


def read_input_file(file_path: str):
    with open(file_path, mode="r", encoding="utf-8") as input_file:
        return input_file.readlines()


def word_to_digit(word):
    word_digit_pairs = [
        ("one", "1"),
        ("two", "2"),
        ("three", "3"),
        ("four", "4"),
        ("five", "5"),
        ("six", "6"),
        ("seven", "7"),
        ("eight", "8"),
        ("nine", "9"),
    ]
    digit_word_indices = []
    for word_digit in word_digit_pairs:
        count = word.count(word_digit[0])
        start_index = 0
        for _ in range(count):
            index = word.find(word_digit[0], start_index)
            if index != -1:
                digit_word_indices.append((index, word_digit))
                start_index = index + 1
    digit_word_indices.sort()

    if digit_word_indices:
        first_word = digit_word_indices[0][1][0]
        first_digit = digit_word_indices[0][1][1]
        last_word = digit_word_indices[-1][1][0]
        last_digit = digit_word_indices[-1][1][1]
        if first_word != last_word:
            word = word.replace(first_word, first_digit, 1)
            word = word[::-1].replace(last_word[::-1], last_digit, 1)[::-1]
        else:
            word = word.replace(first_word, first_digit)
    return word


def sum_calibration_values_v2(input_lines):
    sum_values = 0
    for line in input_lines:
        line = word_to_digit(line)
        digits = [char for char in line if char.isdigit()]
        if digits:
            first_digit = digits[0]
            last_digit = digits[-1]
            calibration_value = int(first_digit + last_digit)
            sum_values += calibration_value
    return sum_values


if __name__ == "__main__":
    input_path = Path(__file__).parent / "input.txt"

    lines = read_input_file(input_path)

    print(sum_calibration_values(lines))

    print(sum_calibration_values_v2(lines))
