import time
from app.template import get_example, get_input, submit, ints
import numpy as np


def next_line(line: list[int]) -> list[int]:
    stockage_lines = [line]
    diff = line

    while np.count_nonzero(diff) != 0:
        diff = np.diff(diff).tolist()
        stockage_lines.append(diff)

    return stockage_lines


def add_zero_at_end(stockage_lines: list[list[int]]) -> list[list[int]]:
    for line in stockage_lines:
        line.append(0)

    return stockage_lines


def add_zero_at_beginning(stockage_lines: list[list[int]]) -> list[list[int]]:
    for line in stockage_lines:
        line.insert(0, 0)

    return stockage_lines


def predict(stockage_lines: list[list[int]]) -> list[int]:
    stockage_lines_with_zero = add_zero_at_end(stockage_lines)[::-1]

    for index, line in enumerate(stockage_lines_with_zero[:-1]):
        stockage_lines_with_zero[index + 1][-1] = (
            stockage_lines_with_zero[index + 1][-2] + line[-1]
        )

    result = stockage_lines_with_zero[::-1][0][-1]

    return result


def predict_part_2(stockage_lines: list[list[int]]) -> list[int]:
    stockage_lines_with_zero = add_zero_at_beginning(stockage_lines)[::-1]

    for index, line in enumerate(stockage_lines_with_zero[:-1]):
        stockage_lines_with_zero[index + 1][0] = (
            stockage_lines_with_zero[index + 1][1] - line[0]
        )

    result = stockage_lines_with_zero[::-1][0][0]

    return result


if __name__ == "__main__":
    DAY = 9
    PART = 2
    exemple_or_real = int(input("Exemple (0) ou Réel (1) ? "))

    if exemple_or_real == 0:
        s = get_example(DAY).strip()
    else:
        s = get_input(DAY).strip()

    begin_time = time.perf_counter()

    lines = s.splitlines()
    lines_ints = [ints(line) for line in lines]

    next_lines = [next_line(line_int) for line_int in lines_ints]

    ans = 0
    for line in next_lines:
        ans += predict_part_2(line)

    # fin du code
    end_time = time.perf_counter()
    print(f"Temps d'exécution : {end_time - begin_time:.2f} secondes")
    if exemple_or_real == 1:
        submit(DAY, PART, ans)
    else:
        print(ans)
