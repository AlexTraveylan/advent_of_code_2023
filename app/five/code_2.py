from pathlib import Path
from numba import njit
import numpy as np
from app.five.code import Almanac

from app.main import read_input_file


@njit
def seed_to_location_numba(seed: np.int64, convert_maps: np.ndarray) -> np.int64:
    result = seed
    for convert_map in convert_maps:
        result = get_numba(result, convert_map)
    return result


@njit
def get_numba(source_value: np.int64, convertisseur: np.ndarray) -> np.int64:
    for convert in convertisseur:
        if convert[1] <= source_value <= convert[1] + convert[2] - 1:
            return source_value + (convert[0] - convert[1])
    return source_value


@njit
def mininum_location(almac):
    return np.min(
        np.array([seed_to_location_numba(seed, almac[1]) for seed in almac[0]])
    )


@njit
def optimize_seeds(reformatted_seeds, convert_map):
    seeds_starts = [
        seed for index, seed in enumerate(reformatted_seeds) if index % 2 == 0
    ]
    ranges = [rng for index, rng in enumerate(reformatted_seeds) if index % 2 == 1]

    minumums = []
    for index, (seed_start, rng) in enumerate(zip(seeds_starts, ranges)):
        serie = [seed_start + i for i in range(rng)]
        min_serie = min(
            np.array([seed_to_location_numba(seed, convert_map) for seed in serie])
        )
        minumums.append(min_serie)

    return minumums

    # Conversion of normal arrays to numba supported ndarrays


if __name__ == "__main__":
    input_path = Path(__file__).parent / "input.txt"

    lines = read_input_file(input_path)
    lines_without_backslash_n = [line.replace("\n", "") for line in lines]

    almac_ob = Almanac.from_lines(lines_without_backslash_n)

    reformatted_seeds = np.array(almac_ob.seeds, dtype=np.int64)

    max_len = max(
        [len(convert_map.convertisseurs) for convert_map in almac_ob.convert_maps]
    )

    reformatted_convertmaps = np.empty(
        (len(almac_ob.convert_maps), max_len, 3), dtype=np.int64
    )

    for i, convert_map in enumerate(almac_ob.convert_maps):
        for j, conv in enumerate(convert_map.convertisseurs):
            reformatted_convertmaps[i][j] = np.array(
                [
                    conv.destination_range_start,
                    conv.source_range_start,
                    conv.range_length,
                ],
                dtype=np.int64,
            )

    result = optimize_seeds(reformatted_seeds, reformatted_convertmaps)

    print(min(result))
