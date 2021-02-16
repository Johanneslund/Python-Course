#!/usr/bin/env python

""" DT179G - LAB ASSIGNMENT 3
You find the description for the assignment in Moodle, where each detail regarding requirements
are stated. Below you find the inherent code, some of which fully defined. You add implementation
for those functions which are needed:

 - create_logger()
 - measurements_decorator(..)
 - fibonacci_memory(..)
 - print_statistics(..)
 - write_to_file(..)
"""

from pathlib import Path
from timeit import default_timer as timer
from functools import wraps
import argparse
import logging
import logging.config
import json

__version__ = '1.0'
__desc__ = "Program used for measuríng execution time of various Fibonacci implementations!"

LINE = '\n' + ("---------------" * 5)
RESOURCES = Path(__file__).parent / "../_Resources/"
LOGGER = None  # declared at module level, will be defined from main()


def create_logger() -> logging.Logger:
    """Create and return logger object."""

    """Gets the JSON file"""
    jsonfile = RESOURCES / "ass3_log_conf.json"
    with open(jsonfile) as json_file:
        data = json.load(json_file)

    """Configures and return the logger"""
    logging.config.dictConfig(data)
    logger = logging.getLogger("ass_3_logger")
    return logger


def measurements_decorator(func):
    """Function decorator, used for time measurements."""

    @wraps(func)
    def wrapper(nth_nmb: int) -> tuple:
        """Create list and sets start time"""
        list = []
        starttime = timer()
        """Adding info in logger"""
        LOGGER.info("Starting measurements...")

        while nth_nmb >= 0:
            """Adds value to container"""
            list.append(func(nth_nmb))
            """Logs every fifth iteration"""
            if (nth_nmb % 5) == 0:
                LOGGER.debug('{}: {}'.format(nth_nmb, func(nth_nmb)))
            nth_nmb -= 1
        endtime = timer()
        """Calculates the time of the calculation"""
        duration = endtime - starttime

        return duration, list

    return wrapper


@measurements_decorator
def fibonacci_iterative(nth_nmb: int) -> int:
    """An iterative approach to find Fibonacci sequence value.
    YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""
    old, new = 0, 1
    if nth_nmb in (0, 1):
        return nth_nmb
    for __ in range(nth_nmb - 1):
        old, new = new, old + new
    return new


@measurements_decorator
def fibonacci_recursive(nth_nmb: int) -> int:
    """An recursive approach to find Fibonacci sequence value.
    YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""

    def fib(_n):
        return _n if _n <= 1 else fib(_n - 1) + fib(_n - 2)

    return fib(nth_nmb)


@measurements_decorator
def fibonacci_memory(nth_nmb: int) -> int:
    """An recursive approach to find Fibonacci sequence value, storing those already calculated."""

    """Where every number will be stored"""
    memory = {0: 0, 1: 1}

    """Algorithm, which calls for itself if the number that is sent in is not present in the memory"""
    def fib(_n):
        if _n <= 1:
            return _n
        elif _n not in memory:
            number = (list(memory.values())[-1] + list(memory.values())[-2])
            memory[(list(memory.keys())[-1] + 1)] = number
            return fib(_n)
        else:
            return list(memory.values())[-1]

    return fib(nth_nmb)


def duration_format(duration: float, precision: str) -> str:
    """Function to convert number into string. Switcher is dictionary type here.
    YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""
    switcher = {
        'Seconds': "{:.5f}".format(duration),
        'Milliseconds': "{:.5f}".format(duration * 1_000),
        'Microseconds': "{:.1f}".format(duration * 1_000_000),
        'Nanoseconds': "{:d}".format(int(duration * 1_000_000_000))
    }

    # get() method of dictionary data type returns value of passed argument if it is present in
    # dictionary otherwise second argument will be assigned as default value of passed argument
    return switcher.get(precision, "nothing")


def print_statistics(fib_details: dict, nth_value: int):
    """Function which handles printing to console."""

    header = ["Seconds", "Milliseconds", "Microseconds", "Nanoseconds"]
    heads = ""
    tabel_data = []

    """Prints the first statement and the line"""
    print("{0}\n{1}{0}".format(LINE, f"DURATION FOR EACH APPROACH WITHIN INTERVAL: {nth_value}-0".center(len(LINE))))

    """Prints and formats each time-format"""
    for head in header:
        heads += '{:>15}'.format(head)
    print('{:13} {} '.format("", heads))

    """Adds both name of method and the values to table"""
    for items, keys in fib_details.items():
        value = ""
        for head in header:
            temp_value = duration_format(keys[0], head)
            value += '{:>15}'.format(temp_value)
            """Appends it to table"""
        tabel_data.append([
            items.title(),
            value
        ])

    """Prints and formats the name and values of each method"""
    for i in range(len(tabel_data)):
        print("{: <13} {}".format(*tabel_data[i]))


def write_to_file(fib_details: dict):
    """Function to write information to file."""

    """Get the file name"""
    RESOURCES / "ass3_log_conf.json"

    """Loops through every fib_detail"""
    for name, values in fib_details.items():
        count = len(values[1]) - 1
        string = (str(name).replace(" ", "_") + ".txt")
        file = open(RESOURCES / string, "w")
        """Loops through every value in each fib_detail and adds it to the file"""
        for value in values[1]:
            file.write(str(count) + ": " + str(value) + "\n")
            count -= 1
        file.close()


def main():
    """The main program execution. YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""
    epilog = "DT179G Assignment 3 v" + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('nth', metavar='nth', type=int, nargs='?', default=30,
                        help="nth Fibonacci sequence to find.")

    global LOGGER  # ignore warnings raised from linters, such as PyLint!
    LOGGER = create_logger()

    args = parser.parse_args()
    nth_value = args.nth  # nth value to sequence. Will fallback on default value!

    fib_details = {  # store measurement information in a dictionary
        'fib iteration': fibonacci_iterative(nth_value),
        'fib recursion': fibonacci_recursive(nth_value),
        'fib memory': fibonacci_memory(nth_value)
    }

    print_statistics(fib_details, nth_value)  # print information in console
    write_to_file(fib_details)  # write data files


if __name__ == "__main__":
    main()
