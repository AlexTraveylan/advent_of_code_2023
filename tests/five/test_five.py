from app.five.code import Almanac, ConvertLine, ConvertMap


ENONCE = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


def test_convert_line():
    line = "50 98 2"
    assert ConvertLine.from_line(line).destination_range_start == 50
    assert ConvertLine.from_line(line).source_range_start == 98
    assert ConvertLine.from_line(line).range_length == 2


def test_convert_map():
    lines = "seed-to-soil map:", "50 98 2", "52 50 48"
    convert_map = ConvertMap.from_lines(lines)

    assert convert_map.title == "seed-to-soil map"
    assert len(convert_map.convertisseurs) == 2
    assert convert_map.convert_role == ("seed", "soil")


def test_almanac():
    lines = ENONCE.splitlines()
    almanac = Almanac.from_lines(lines)

    assert almanac.seeds == [79, 14, 55, 13]
    assert len(almanac.convert_maps) == 7

    assert almanac.convert_maps[0].title == "seed-to-soil map"
    assert almanac.convert_maps[-1].title == "humidity-to-location map"

    assert almanac.convert_maps[0].convertisseurs[0].destination_range_start == 50
    assert almanac.convert_maps[0].convertisseurs[0].source_range_start == 98
    assert almanac.convert_maps[0].convertisseurs[0].range_length == 2
