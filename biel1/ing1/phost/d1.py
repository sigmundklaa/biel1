
import math
import time
import enum
import colorsys
import functools
from typing import (
    Literal,
    Set,
    Tuple
)
from sense_hat import SenseHat

Step = Literal[-1, 1]
Level = Literal[1, 2, 3]
Point = Tuple[int, int]

GRID_SIZE = 8
INVALID_DIR = 'invalid direction {}'


class Direction(enum.Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    LT = 4  # left-top
    RT = 5  # right-top
    RB = 6  # right-bottom
    LB = 7  # left-bottom


class Stabilizer:
    _sense: SenseHat

    def __init__(self, sense: SenseHat):
        self._sense = sense

    def _start(self, step: Step) -> int:
        return 0 if step == 1 else GRID_SIZE - 1

    def make_arrow_part(self,
                        level: Level,
                        step_x: Step,
                        step_y: Step) -> Set[Point]:

        level_invert = 3 - level
        offset_x = self._start(step_x) + (level_invert * step_x)
        offset_y = self._start(step_y) + (4 * step_y)

        ret = set({(offset_x, offset_y)})

        for _ in range(1, level + 1):
            offset_x += step_x
            offset_y += step_y

            ret.add((offset_x, offset_y))

        return ret

    def make_corner_part(self,
                         level: Level,
                         const_x: bool,
                         step_x: Step,
                         step_y: Step) -> Set[Point]:

        level_invert = 3 - level

        step_const = step_x if const_x else step_y
        offset_const = self._start(step_const) + (level_invert * step_const)

        if const_x:
            return {
                (
                    offset_const,
                    self._start(step_x)
                    + ((level_invert + 1) * step_x)
                    + (i * step_x)
                ) for i in range(level)
            }

        return {
            (
                self._start(step_y)
                + ((level_invert + 1) * step_y)
                + (i * step_y),
                offset_const
            ) for i in range(level)
        }

    def make_corner(self, level: Level, dir_: Direction) -> Set[Point]:
        def _make_union(step_x: Step, step_y: Step) -> Set[Point]:
            xconst = self.make_corner_part(level, True, step_x)
            yconst = self.make_corner_part(level, False, step_y)

            return xconst | yconst | set({(
                list(xconst)[0][0],
                list(yconst)[0][1]
            )})

        steps = {
            Direction.LT: (1, 1),
            Direction.RT: (-1, 1),
            Direction.RB: (-1, -1),
            Direction.LB: (1, -1)
        }

        try:
            return _make_union(*steps[dir_])
        except KeyError:
            raise ValueError(INVALID_DIR.format(dir_))

    def make_arrow(self, level: Level, dir_: Direction) -> Set[Point]:
        def _make_union(
                arg1: Tuple[Step],
                arg2: Tuple[Step]) -> Set[Point]:
            return self.make_arrow_part(
                level, *arg1).union(
                self.make_arrow_part(level, *arg2))

        steps = {
            Direction.LEFT: ((1, -1), (1, 1)),
            Direction.UP: ((1, -1), (-1, -1)),
            Direction.RIGHT: ((-1, 1), (-1, -1)),
            Direction.DOWN: ((-1, -1), (1, -1))
        }

        try:
            return _make_union(*steps[dir_])
        except KeyError:
            raise ValueError(INVALID_DIR.format(dir_))


def main(*args) -> None:
    sense = SenseHat()

    p = Stabilizer(sense)

    while 1:
        for x in p.make_arrow(1, Direction.RIGHT):
            p._sense.set_pixel(*(list(x) + [255, 0, 255]))

        time.sleep(1)
        p._sense.clear()


if __name__ == '__main__':
    import sys

    main(*sys.argv[1:])
