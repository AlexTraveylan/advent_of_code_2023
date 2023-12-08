from app.heigth.part_1 import Parser, execute_instructions


lines = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""


def test_execute_instructions():
    parser = Parser.from_lines(lines.splitlines())
    assert execute_instructions(parser) == 6
