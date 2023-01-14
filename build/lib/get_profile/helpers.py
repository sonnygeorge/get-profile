import cProfile
import itertools
import types
from typing import List

import pandas as pd
import numpy as np


def get_profiling_stats(pr: cProfile.Profile) -> pd.DataFrame:
    code_to_str = np.vectorize(
        lambda x: f"CALLABLE: {x.co_name}\nLINENO: {x.co_firstlineno}\nFILE: {x.co_filename}"
        if isinstance(x, types.CodeType)
        else str(x)
    )
    caller_to_str = np.vectorize(
        lambda x: "\n\n".join(
            list(code_to_str(list(map(lambda s_entry: s_entry.code, x))))
        )
        if x
        else ""
    )
    df = (
        pd.DataFrame(
            pr.getstats(),
            columns=[
                "func",
                "ncalls",
                "ccalls",
                "tottime",
                "cumtime",
                "callees",
            ],
        )
        .query("tottime > .005")
        .sort_values(by="tottime", ascending=False)
        .head(15)
        .drop(columns=["ccalls"])
        .assign(
            rpercall=lambda x: np.round(x.tottime / x.ncalls, 4),
            percall=lambda x: np.round(x.cumtime / x.ncalls),
            rtottime=lambda x: np.round(x.tottime, 4),
            tottime=lambda x: np.round(x.cumtime, 4),
            func=lambda x: code_to_str(x.func),
            callees=lambda x: caller_to_str(x.callees),
        )
        .rename(columns={"rtottime": "tottime -r", "rpercall": "percall -r"})
        .reset_index(drop=True)
    )[
        [
            "func",
            "ncalls",
            "tottime -r",
            "percall -r",
            "tottime",
            "percall",
            "callees",
        ]
    ]
    return df


def get_readable_grid(two_d_array, max_col_widths: List[int]) -> str:
    """takes a 2d array and returns a grid-like, readable string"""
    header_div_char = "="
    hor_div_char = "-"
    vert_div_char = "|"

    if isinstance(two_d_array, pd.DataFrame):
        two_d_array = [list(two_d_array.columns)] + two_d_array.values.tolist()
        header = True
    else:
        header = False

    if len(two_d_array[0]) != len(max_col_widths):
        raise ValueError(
            f"Number of columns in two_d_array ({len(two_d_array[0])}) "
            f"does not match number of columns in max_col_widths ({len(max_col_widths)})"
        )

    col_widths = [max(len(str(val)) for val in col) for col in zip(*two_d_array)]
    col_widths = [min(max, width) for width, max in zip(col_widths, max_col_widths)]
    grid_width = sum(col_widths) + (len(two_d_array[0]) - 1) * 3 + 4

    def wrap_str(s, wrap_width):
        rigid_wrap = lambda x: [
            x[i : i + wrap_width] for i in range(0, len(x), wrap_width)
        ]
        l = s.split("\n")
        l = [rigid_wrap(s) if len(s) > 0 else [""] for s in l]
        return sum(l, [])

    def increment_row_to_grid(grid, row, hor_div_char, vert_div_char, col_widths):
        row = [wrap_str(str(s), width) for s, width in zip(row, col_widths)]
        transposed_row = list(itertools.zip_longest(*row, fillvalue=""))
        for row in transposed_row:
            grid += f"\n{vert_div_char}"
            for val, width in zip(row, col_widths):
                grid += f" {val.ljust(width)} {vert_div_char}"
        return grid + "\n" + hor_div_char * grid_width

    # add dataframe header to grid if applicable
    if header:
        grid = header_div_char * grid_width
        grid = increment_row_to_grid(
            grid, two_d_array[0], header_div_char, vert_div_char, col_widths
        )
        two_d_array = two_d_array[1:]
    else:
        grid = hor_div_char * grid_width

    # fill in the rest of the grid
    for row in two_d_array:
        grid = increment_row_to_grid(grid, row, hor_div_char, vert_div_char, col_widths)

    return grid
