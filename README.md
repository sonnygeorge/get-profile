# get-profile

A simple library to inject the most profiling bang-for-buck into a single line of code (decorator).

I.E.

```python
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


if __name__ == '__main__':
    your_program()
```
Would print something like this after your program has run:

```
Profiling results for "your_program":

===============================================================================================================================
| func                      | ncalls | tottime -r | percall -r | tottime | percall | callees                                  |
===============================================================================================================================
| CALLABLE: your_program    | 1      | 3.0073     | 3.0073     | 0.0003  | 0.0     | CALLABLE: your_function_a                |
| LINENO: 13                |        |            |            |         |         | LINENO: 6                                |
| FILE: /Users/sonnygeorge/ |        |            |            |         |         | FILE: /Users/sonnygeorge/get-profile/exa |
| get-profile/example.py    |        |            |            |         |         | mple.py                                  |
|                           |        |            |            |         |         |                                          |
|                           |        |            |            |         |         | CALLABLE: your_function_b                |
|                           |        |            |            |         |         | LINENO: 9                                |
|                           |        |            |            |         |         | FILE: /Users/sonnygeorge/get-profile/exa |
|                           |        |            |            |         |         | mple.py                                  |
-------------------------------------------------------------------------------------------------------------------------------
| <built-in method time.sle | 2      | 3.007      | 1.5035     | 3.007   | 2.0     |                                          |
| ep>                       |        |            |            |         |         |                                          |
-------------------------------------------------------------------------------------------------------------------------------
| CALLABLE: your_function_b | 1      | 2.002      | 2.002      | 0.0     | 0.0     | <built-in method time.sleep>             |
| LINENO: 9                 |        |            |            |         |         |                                          |
| FILE: /Users/sonnygeorge/ |        |            |            |         |         |                                          |
| get-profile/example.py    |        |            |            |         |         |                                          |
-------------------------------------------------------------------------------------------------------------------------------
| CALLABLE: your_function_a | 1      | 1.005      | 1.005      | 0.0     | 0.0     | <built-in method time.sleep>             |
| LINENO: 6                 |        |            |            |         |         |                                          |
| FILE: /Users/sonnygeorge/ |        |            |            |         |         |                                          |
| get-profile/example.py    |        |            |            |         |         |                                          |
-------------------------------------------------------------------------------------------------------------------------------
```


Installation
------------
``get-profile`` can be installed with ``pip``:

    $ pip install get-profile


Decorator Parameters
--------------------

Release 0.0.2 supports the following parameters for the get_profile decorator:

```python
get_profile(

# topn limits the table to only the top n rows
top_n: int = 10,

# only_my_functions = True will filter out functions whose 
# "func" field contains the regex pattern: 
# r"/python[0-9]+\.[0-9]+/|<.*>",
# (a hacky way to limit the output to just your own functions)
only_my_functions: bool = False,  

# sort_by is the column you would like to sort by (descending)
sort_by: str = "tottime -r",

# min_col is the column you would like to filter by (min_val)
min_col: str = "tottime -r",

# min_val is the minimum value for the min_col
min_val: float = 0.005,

# output_width is the width in chars of the output table
output_width: int = 150,

# toggles whether or not the "calees" column is printed
callees: bool = True,

)
```
