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
``get-profile`` can be installed with ``pip``::

    $ pip install get-profile
