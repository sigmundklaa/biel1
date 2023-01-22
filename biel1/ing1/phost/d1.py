"""
Arrow that displays direction to tilt the PI in order to stabilize it.
Roll was giving bad values, so currently only pitch is used.
"""


import time
import enum
from typing import (
    Literal,
    Set,
    Tuple
)
from sense_hat import SenseHat


class Direction(enum.IntEnum):
    """
    Enum containing the directon values used by the arrow
    """
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    LT = 4  # left-top
    RT = 5  # right-top
    RB = 6  # right-bottom
    LB = 7  # left-bottom
    NONE = 8


Step = Literal[-1, 1]
Level = Literal[1, 2, 3]
Point = Tuple[int, int]
GyroVals = Tuple[int, int, int]
StabState = Tuple[Level, Direction]

GRID_SIZE = 8
INVALID_DIR = 'invalid direction {}'


def abs_get_sign(num: int) -> Tuple[int, int]:
    if num < 0:
        return (-1 * num), 1

    return num, 0


class Stabilizer:
    """
    Main stabilizer class
    """
    _sense: SenseHat
    _rel: GyroVals

    def __init__(self, sense: SenseHat):
        self._sense = sense
        self._rel = self._sense.get_orientation_degrees()

    def resolve_state(self, diff: int, dirs_: Tuple[Direction, Direction]) -> StabState:
        if not (10 < diff < 350):
            return (0, Direction.NONE)
        elif diff > 180:
            diff = -1 * (360 - diff)

        sign = 1 if diff < 0 else 0

        return min(((abs(diff) // 60) + 1), 3), dirs_[1 - sign]

    def resolve_corner_dir(self, dir1: Direction, dir2: Direction) -> Direction:
        return {
            (Direction.UP, Direction.LEFT): Direction.LT,
            (Direction.UP, Direction.RIGHT): Direction.RT,
            (Direction.DOWN, Direction.RIGHT): Direction.RB,
            (Direction.DOWN, Direction.LEFT): Direction.LB
        }[(dir1, dir2)]

    def run(self):
        """
        Main function responsible for displaying the arrow
        according to current orientation
        """
        def _get_state():
            pitch, roll, _ = map(
                int, self._sense.get_orientation_degrees().values())

            #print(pitch, roll)

            dp, dr = pitch, roll  # pitch - self._rel[0], roll - self._rel[1]

            statep = self.resolve_state(dp, [Direction.DOWN, Direction.UP])

            return statep

        state = _get_state()

        self._sense.clear()

        if state[0] == 0 or state[1] == Direction.NONE:
            return

        for x in self.make(*state):
            self._sense.set_pixel(*(list(x) + [255, 0, 255]))

    def _start(self, step: Step) -> int:
        """
        Get starting point for the arrow
        As a negative step moves backwards, the starting point
        is the end of the display for step == -1 
        """
        return 0 if step == 1 else GRID_SIZE - 1

    def make_arrow_part(self,
                        level: Level,
                        step_x: Step,
                        step_y: Step) -> Set[Point]:
        """
        Make one half of the arrow
        Called by self.make_arrow(...) two times in order to
        make a full arrow
        """

        # Level 3 should give an offset of 0,
        # as it starts on the very end of the display
        # Level 2 starts 1 in, etc.

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

        # Level 3 should give an offset of 0,
        # as it starts on the very end of the display
        # Level 2 starts 1 in, etc.
        level_invert = 3 - level

        step_const = step_x if const_x else step_y

        # Create the constant offset for the coordinate that is not moving (either x or y)
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
        """
        Make a full corner
        Not used as the PI was not giving correct roll values,
        but would be used when a tilt in two directions simaltaneousyl
        was required to stabilize the PI.
        """
        def _make_union(step_x: Step, step_y: Step) -> Set[Point]:
            xconst = self.make_corner_part(level, True, step_x, step_y)
            yconst = self.make_corner_part(level, False, step_x, step_y)

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
            Direction.DOWN: ((-1, 1), (1, 1))
        }

        try:
            return _make_union(*steps[dir_])
        except KeyError:
            raise ValueError(INVALID_DIR.format(dir_))

    def make(self, level: Level, dir_: Direction) -> Set[Point]:
        """
        Calls make_corner or make_arrow, depending on direction.
        Currently only calls make_arrow
        """
        assert level in [1, 2, 3], 'invalid level %i' % level
        assert dir_ in [d.value for d in Direction], INVALID_DIR.format(dir_)

        if dir_ <= Direction.DOWN:
            return self.make_arrow(level, dir_)

        return self.make_corner(level, dir_)


def main(*args) -> None:
    sense = SenseHat()

    p = Stabilizer(sense)

    while 1:
        p.run()
        # time.sleep(0.2)


if __name__ == '__main__':
    import sys

    main(*sys.argv[1:])
