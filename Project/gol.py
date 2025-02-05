#!/usr/bin/env python
"""
The universe of the Game of Life is an infinite two-dimensional orthogonal grid of square cells,
each of which is in one of two possible states, alive or dead (populated or unpopulated).
Every cell interacts with its eight neighbours, which are the cells that are horizontally,
vertically, or diagonally adjacent.

At each step in time, the following transitions occur:

****************************************************************************************************
   1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
   2. Any live cell with two or three live neighbours lives on to the next generation.
   3. Any live cell with more than three live neighbours dies, as if by overpopulation.
   4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
****************************************************************************************************

The initial pattern constitutes the seed of the system.

The first generation is created by applying the above rules simultaneously to every cell in the
seed—births and deaths occur simultaneously, and the discrete moment at which this happens is
sometimes called a tick. The rules continue to be applied repeatedly to create further generations.

You run this script as a module:
    python -m Project.gol.py
"""

import argparse
import ast
import random
import json
import logging
import itertools
from pathlib import Path
from ast import literal_eval
from time import sleep

import Project.code_base as cb

__version__ = '1.0'
__desc__ = "A simplified implementation of Conway's Game of Life."

RESOURCES = Path(__file__).parent / "../_Resources/"


# -----------------------------------------
# IMPLEMENTATIONS FOR HIGHER GRADES, C - B
# -----------------------------------------

def load_seed_from_file(_file_name: str) -> tuple:
    """ Load population seed from file. Returns tuple: population (dict) and world_size (tuple). """

    """Just some code I tried, tried to go for C as a grade but didnt have the time """
    pass
    file = 'seed_gliders.json'
    jsonfile = RESOURCES / Path(file)
    with open(jsonfile) as json_file:
        data = json.load(json_file)

    pop: dict = {}

    for x in data['population']:
        if x is not None:
            pop[x] = data['population'][x]
        else:
            pop[x] = x

    for x in pop:
        print(x)

    b = [eval(elem) for elem in pop]

    print(b)
    return None, None


def create_logger() -> logging.Logger:
    """ Creates a logging object to be used for reports. """
    pass


def simulation_decorator(func):
    """ Function decorator, used to run full extent of simulation. """
    pass


# -----------------------------------------
# BASE IMPLEMENTATIONS
# -----------------------------------------

def parse_world_size_arg(_arg: str) -> tuple:
    """ Parse width and height from command argument. """

    try:
        """"Splits the numbers at the x"""
        numbers = [int(i) for i in _arg.split('x')]

        """Checks if the amount of numbers is correct"""
        if len(numbers) != 2:
            raise AssertionError

        """Checks if the number is les than one and raises error if that is the case """
        for number in numbers:
            if number < 1:
                raise ValueError

        return numbers

    except AssertionError as e:
        print("World size should contain width and height, separated by ‘x’. Ex: ‘80x40’")
        print("Using default world size: 80x40")
        value = (80, 40)
        return value

    except ValueError as error:
        first = "Both width and height needs to have positive values above zero."
        print(error) if (len(str(error)) > 0) else print(first)
        print("Using default world size: 80x40")
        value = (80, 40)
        return value


def populate_world(_world_size: tuple, _seed_pattern: str = None) -> dict:
    """ Populate the world with cells and initial states. """
    """Creates the containers """
    pop: dict = {}
    pattern: list = []
    """Checks if pattern is present"""
    if _seed_pattern:
        pattern = cb.get_pattern(_seed_pattern, _world_size)

    """Gets the coordinates"""
    coordinates = list(itertools.product(range(0, _world_size[1]), range(0, _world_size[0])))

    """Creates the starting pattern of the world, depending if the pattern in used or not"""
    for i in range(len(coordinates)):
        if coordinates[i][0] == 0 \
                or coordinates[i][0] == _world_size[1] - 1 \
                or coordinates[i][1] == 0 \
                or coordinates[i][1] == _world_size[0] - 1:
            pop[coordinates[i]] = None
        else:
            if pattern:
                pop[coordinates[i]] = {
                    "state": cb.STATE_ALIVE if coordinates[i] in pattern else cb.STATE_DEAD,
                    "neighbours": calc_neighbour_positions(coordinates[i])
                }
            else:
                pop[coordinates[i]] = {
                    "state": cb.STATE_ALIVE if random.randint(0, 21) >= 15 else cb.STATE_DEAD,
                    "neighbours": calc_neighbour_positions(coordinates[i])
                }

    return pop


def calc_neighbour_positions(_cell_coord: tuple) -> list:
    """ Calculate neighbouring cell coordinates in all directions (cardinal + diagonal).
    Returns list of tuples. """

    """Creates and returns coordinates of all cells around the current cell"""
    neighbour: list = [
        (_cell_coord[0] - 1, _cell_coord[1] - 1),
        (_cell_coord[0] - 1, _cell_coord[1]),
        (_cell_coord[0] - 1, _cell_coord[1] + 1),
        (_cell_coord[0], _cell_coord[1] - 1),
        (_cell_coord[0], _cell_coord[1] + 1),
        (_cell_coord[0] + 1, _cell_coord[1] - 1),
        (_cell_coord[0] + 1, _cell_coord[1]),
        (_cell_coord[0] + 1, _cell_coord[1] + 1)
    ]
    return neighbour


def run_simulation(_generations: int, _population: dict, _world_size: tuple):
    """ Runs simulation for specified amount of generations. """

    cb.clear_console()
    """Gets the population"""
    _population = update_world(_population, _world_size)
    sleep(0.2)

    """The recursive method, that calls for itself"""
    if _generations > 0:
        run_simulation(_generations - 1, _population, _world_size)


def update_world(_cur_gen: dict, _world_size: tuple) -> dict:
    """ Represents a tick in the simulation. """
    nextgen: dict = {}

    """Adds the rim"""
    for k in _cur_gen:
        print_string = cb.get_print_value(cb.STATE_RIM) if _cur_gen[k] is None \
            else cb.get_print_value(_cur_gen[k]["state"])
        cb.progress(print_string + '\n' if k[1] == _world_size[0] - 1 else print_string)

        if _cur_gen[k] is None:
            nextgen[k] = None

            """Checks whether the cell will stay alive or has died"""
        else:
            alive = count_alive_neighbours(_cur_gen[k]['neighbours'], _cur_gen)
            if _cur_gen[k]['state'] == "X" and 2 <= alive <= 3:
                nextgen[k] = {
                    "state": cb.STATE_ALIVE,
                    "neighbours": _cur_gen[k]['neighbours']
                }
            elif _cur_gen[k]['state'] == "-" and alive == 3:
                nextgen[k] = {
                    "state": cb.STATE_ALIVE,
                    "neighbours": _cur_gen[k]['neighbours']
                }
            else:
                nextgen[k] = {
                    "state": cb.STATE_DEAD,
                    "neighbours": _cur_gen[k]['neighbours']
                }
    return nextgen


def count_alive_neighbours(_neighbours: list, _cells: dict) -> int:
    """ Determine how many of the neighbouring cells are currently alive. """
    alive: int = 0
    count = 0

    """Checks the list of neighbours and counts the amount that is alive"""
    for c in _neighbours:
        if _cells[c] is not None and _cells[c]["state"] == "X":
            alive += 1

    return alive


def main():
    """ The main program execution. YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!! """
    epilog = "DT179G Project v" + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('-g', '--generations', dest='generations', type=int, default=50,
                        help='Amount of generations the simulation should run. Defaults to 50.')
    parser.add_argument('-s', '--seed', dest='seed', type=str,
                        help='Starting seed. If omitted, a randomized seed will be used.')
    parser.add_argument('-ws', '--worldsize', dest='worldsize', type=str, default='80x40',
                        help='Size of the world, in terms of width and height. Defaults to 80x40.')
    parser.add_argument('-f', '--file', dest='file', type=str,
                        help='Load starting seed from file.')

    args = parser.parse_args()

    try:
        if not args.file:
            raise AssertionError
        population, world_size = load_seed_from_file(args.file)
    except (AssertionError, FileNotFoundError):
        world_size = parse_world_size_arg(args.worldsize)
        population = populate_world(world_size, args.seed)

    run_simulation(args.generations, population, world_size)


if __name__ == "__main__":
    main()
