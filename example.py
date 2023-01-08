import time

from get_profile import get_profile


def your_function_a():
    time.sleep(1)


def your_function_b():
    time.sleep(2)


@get_profile
def your_program():
    your_function_a()
    your_function_b()


if __name__ == "__main__":
    your_program()
