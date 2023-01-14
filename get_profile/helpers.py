import cProfile
import itertools
import types
from typing import List
import warnings


import pandas as pd
import numpy as np


def get_profiling_stats(
    pr: cProfile.Profile,
    top_n: int = 15,
    only_my_functions: bool = False,
    sort_by: str = "tottime -r",
    min_col: str = "tottime -r",
    min_val: float = 0.005,
    callees: bool = True,
) -> pd.DataFrame:
    code_to_str = np.vectorize(
        lambda x: f"CALLABLE: {x.co_name}\nLINENO: {x.co_firstlineno}\nFILE: {x.co_filename}\nTEST: {'none'}"
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
    df = pd.DataFrame(
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
    if not callees:
        df = df.drop(columns=["callees"])
    else:
        df = df.assign(callees=lambda x: caller_to_str(x["callees"]))
    df = (
        df.drop(columns=["ccalls"])
        .assign(
            **{
                "percall -r": lambda x: x["tottime"] / x["ncalls"],
                "percall": lambda x: x["cumtime"] / x["ncalls"],
                "tottime -r": lambda x: x["tottime"],
                "tottime": lambda x: x["cumtime"],
                "func": lambda x: code_to_str(x.func),
            }
        )
        .sort_values(by=sort_by, ascending=False)
        .query(f"`{min_col}` > {min_val}")
        .assign(
            **{
                "percall -r": lambda x: np.round(x["percall -r"], 4),
                "percall": lambda x: np.round(x["percall"], 4),
                "tottime -r": lambda x: np.round(x["tottime -r"], 4),
                "tottime": lambda x: np.round(x["tottime"], 4),
            }
        )
    )
    if only_my_functions:
        # remove rows whose "func" contains either a /python*.*/ folder or <.*>
        temp_df = df[~df["func"].str.contains(r"/python[0-9]+\.[0-9]+/|<.*>")]
        if temp_df.empty:
            warnings.warn(
                "get_filter could not filter out functions from native python and installed packages:"
                "the folowing regex pattern must have been found in the file path of your code "
                r"'/python[0-9]+\.[0-9]+/|<.*>'"
            )
        else:
            df = temp_df
    return_cols = [
        "func",
        "ncalls",
        "tottime -r",
        "percall -r",
        "tottime",
        "percall",
    ]
    return_cols = return_cols + ["callees"] if callees else return_cols
    return df.head(top_n)[return_cols]


def get_max_col_widths(max_width: int, callees: bool):
    if callees:
        if max_width < 73:
            warnings.warn(
                "get_profile(callees=True) cannot be shrunk narrower than an output_width of 73 chars"
            )
            max_width = 73
        c1 = int((max_width - 61) * 0.35)
        c7 = int((max_width - 61) * 0.65)
        return [c1, 6, 10, 10, 7, 7, c7]
    else:
        if max_width < 63:
            warnings.warn(
                "get_profile(callees=True) cannot be shrunk narrower than an output_width of 63 chars"
            )
            max_width = 63
        return [max_width - 59, 6, 10, 10, 7, 7]


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
