
import re
import os
import sys
import csv
import time
import functools
from sense_hat import SenseHat
from dataclasses import dataclass, fields
from typing import List
from pathlib import Path

if sys.version_info < (3, 8):
    raise ImportError(
        'Python >= 3.8 is required (got {}, {}, {})'.format(*sys.version_info[:3]))

GRADIENT = -0.0065
ACCEL = 9.81
GASS_CONST = 287.06
SAVE_INTERVAL = 5
KELVIN_BASE = 273.15

DUMPDIR = Path.cwd().joinpath('datadumps')
DUMP_EXT = 'csv'

if not DUMPDIR.exists():
    os.makedirs(DUMPDIR, exist_ok=True)


def _get_dumpfile(p: Path) -> Path:
    max_ = 0
    for f in os.listdir(p):
        if (m := re.match(re.compile(f'^dump_(\\d+)\\.{DUMP_EXT}$'), f)) is not None:
            max_ = int(m.group(1))

    return p.joinpath(f'dump_{max_ + 1}.{DUMP_EXT}')


@dataclass
class Value:
    height: float
    press: float
    refp: float
    refh: float
    reft: float

    #@functools.lru_cache()
    def _base(self) -> List[float]:
        return [getattr(self, field.name) for field in fields(self)]

    def to_list(self) -> List[float]:
        return self._base()

    def __getitem__(self, slice_):
        return self._base()[slice_]

    def __str__(self):
        return str(self._base())


class HeightLogger:
    vals: List[Value]
    refval: Value
    dumpf: Path
    sense: SenseHat

    def __init__(self, sense: SenseHat):
        self.sense = sense
        self.dumpf = _get_dumpfile(DUMPDIR)
        
        pressure = self._get_pressure()
        self.refval = Value(0, pressure, pressure, 0, self._get_temp())
        self.vals = [self.refval]

    def measure(self) -> None:
        pressure = self._get_pressure()

        self.vals.append(Value(
            hypsometric(pressure, *(self.refval[2:])),
            pressure,
            *(self.refval[2:])
        ))

        print(self.vals[-1])

        if (len(self.vals) >= SAVE_INTERVAL) == 0:
            self._write()

    def _get_temp(self) -> float:
        """
        Returns temperature in Kelvin
        """
        return KELVIN_BASE + self.sense.get_temperature()

    def _get_pressure(self) -> float:
        """
        Returns pressure in Pa
        """
        return self.sense.get_pressure() * 100

    def _write(self) -> None:
        with open(self.dumpf, 'a') as fp:
            writer = csv.writer(fp)
            writer.writerows([x.to_list() for x in self.vals])

        self.vals = []


def hypsometric(press: float, refp: float,
                refh: float, reft: float) -> float:
    return (reft / GRADIENT) \
        * (((press / refp) ** (-(GRADIENT * GASS_CONST) / (ACCEL))) - 1) \
        + refh


def main(*args) -> None:
    hl = HeightLogger(SenseHat())

    while 1:
        hl.measure()
        time.sleep(0.1)


if __name__ == '__main__':
    import sys

    main(*sys.argv[1:])
