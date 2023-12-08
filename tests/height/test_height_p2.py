from app.heigth.part_2 import Parser, execute_instructions


lines = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""


def test_execute_instructions():
    parser = Parser.from_lines(lines.splitlines())
    assert execute_instructions(parser) == 6
