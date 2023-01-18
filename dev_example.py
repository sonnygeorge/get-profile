import time

from get_profile import get_profile


class YoMama:
    def heavy(self):
        for i in range(1000):
            time.sleep(0.00001)


def your_function_a():
    time.sleep(0.001)


def your_function_b():
    import numpy as np
    import pandas as pd

    a = []
    for i in range(40):
        x = np.random.random(size=400)
        a.append(x)
    df = pd.DataFrame(a)
    print(df.head(2))
    mami = YoMama()
    mami.heavy()
    time.sleep(0.2)


@get_profile(
    top_n=20,
    only_my_functions=True,
    sort_by="tottime -r",
    min_col="tottime -r",
    min_val=0.001,
    callees=True,
    output_width=80,
)
def your_program():
    your_function_a()
    your_function_b()


if __name__ == "__main__":
    your_program()
