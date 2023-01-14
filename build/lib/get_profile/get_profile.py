import cProfile

from get_profile.helpers import get_profiling_stats, get_readable_grid


def get_profile(func):
    """decorator to get the profiled runtime stats of python code"""

    def decorated_func(*args, **kwargs):
        # profile runtime stats
        with cProfile.Profile() as pr:
            # execute process
            output = func(*args, **kwargs)

            # get runtime stats as a pd.Dataframe
            df = get_profiling_stats(pr)

        # print profile stats
        if not df.empty:
            max_col_widths = [25, 10, 10, 10, 10, 10, 40]
            print(
                f'\nProfiling results for "{func.__name__}":\n\n{get_readable_grid(df, max_col_widths=max_col_widths)}\n'
            )

        return output

    decorated_func.__name__ = func.__name__
    return decorated_func
