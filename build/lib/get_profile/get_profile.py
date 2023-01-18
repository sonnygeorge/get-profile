import cProfile

from get_profile.helpers import (
    get_profiling_stats,
    get_max_col_widths,
    get_readable_grid,
)


# implement arg for a logger
# stdout = True? logfilepath?
# something to limit height... max callees? max depth? show callees = T/F?
# maybe only only show names of callees? not lineno & file


def get_profile(
    top_n: int = 10,
    only_my_functions: bool = False,
    sort_by: str = "tottime -r",
    min_col: str = "tottime -r",
    min_val: float = 0.005,
    output_width: int = 150,
    callees: bool = True,
):
    """meta-decorator to take arguments"""

    def decorator(func):
        """decorator to get the profiled runtime stats of python code"""

        def decorated_func(*args, **kwargs):
            # profile runtime stats
            with cProfile.Profile() as pr:
                # execute process
                output = func(*args, **kwargs)

                # get runtime stats as a pd.Dataframe
                df = get_profiling_stats(
                    pr, top_n, only_my_functions, sort_by, min_col, min_val, callees
                )

            # print profile stats
            if not df.empty:
                max_col_widths = get_max_col_widths(
                    max_width=output_width, callees=callees
                )
                readable_table = get_readable_grid(df, max_col_widths=max_col_widths)
                print(
                    f'\nProfiling results for "{func.__name__}()" '
                    f"called with args {args} and kwargs {kwargs}:"
                    f"\n\n{readable_table}\n"
                )

            return output

        decorated_func.__name__ = func.__name__
        return decorated_func

    return decorator
