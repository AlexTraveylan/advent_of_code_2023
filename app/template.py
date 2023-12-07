"""
Advent of code 2023 template file

Author: Alex Traveylan
Date: 2023-12-06
"""
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

AOC_COOKIE = os.getenv("AOC_COOKIE")

YEAR = "2023"


def get_input(day: int) -> str:
    """Get the input for a given day

    Parameters
    ----------
    day : int
        The day of the puzzle

    Returns
    -------
    str
        The input as a string
    """
    req = requests.get(
        f"https://adventofcode.com/{YEAR}/day/{day}/input",
        headers={"cookie": "session=" + AOC_COOKIE},
        timeout=5,
    )
    return req.text


def get_example(day: int, offset=0) -> str:
    """Get the example input for a given day

    Parameters
    ----------
    day : int
        The day of the puzzle
    offset : int, optional
        The offset of the example (default is 0)

    Returns
    -------
    str
        The input as a string
    """
    req = requests.get(
        f"https://adventofcode.com/{YEAR}/day/{day}",
        headers={"cookie": "session=" + AOC_COOKIE},
        timeout=5,
    )
    return req.text.split("<pre><code>")[offset + 1].split("</code></pre>")[0]


def submit(day: int, level: int, answer: str) -> None:
    """Submit an answer to a puzzle

    Parameters
    ----------
    day : int
        The day of the puzzle
    level : int
        The level of the puzzle
    answer : str
        The answer to submit
    """

    text = "you are about to submit the answer:\n"
    text += f">>>>>>>>>>>>>>>>> {answer}\n"
    text += "Press enter to continue or Ctrl+C to abort."
    input(text)

    data = {"level": str(level), "answer": str(answer)}

    response = requests.post(
        f"https://adventofcode.com/{YEAR}/day/{day}/answer",
        headers={"cookie": "session=" + AOC_COOKIE},
        data=data,
        timeout=5,
    )
    if "You gave an answer too recently" in response.text:
        print("VERDICT : TOO MANY REQUESTS")
    elif "not the right answer" in response.text:
        if "too low" in response.text:
            print("VERDICT : WRONG (TOO LOW)")
        elif "too high" in response.text:
            print("VERDICT : WRONG (TOO HIGH)")
        else:
            print("VERDICT : WRONG (UNKNOWN)")
    elif "seem to be solving the right level." in response.text:
        print("VERDICT : INVALID LEVEL")
    else:
        print("VERDICT : OK !")


def ints(line: str) -> list[int]:
    """Convert a string of ints to a list of ints

    Parameters
    ----------
    line : str
        The string to convert

    Returns
    -------
    list[int]
        The list of ints
    """
    return list(map(int, line.split()))


if __name__ == "__main__":
    DAY = 1
    PART = 1
    # s = get_input(DAY).strip()
    s = get_example(DAY).strip()
    begin_time = time.perf_counter()

    # Your code here
    ans = 123456

    # fin du code
    end_time = time.perf_counter()
    print(f"Temps d'exécution : {end_time - begin_time:.2f} secondes")
    submit(DAY, PART, ans)
