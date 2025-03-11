import numpy as np
import os
import sys
import pathlib
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent.resolve(), "../utils/"))
from read_cmdline import read_cmdline
from read_radial_profile import read_radial_profile


def main(basedir, time, simulation, weight, tail):
    radialdir = os.path.join(basedir, "profiles/radial/")

    print(f"######### {simulation} #########")

    fnum = int(time * 2 / 100)
    _, _, _, density_hot, _, temp_hot, _, _, _, _ = read_radial_profile(radialdir, fnum, simulation, "hot", weight, tail)

    print(f"Hot-phase density: {density_hot[1][-1]:.1e}")
    print(f"Hot-phase temperature: {temp_hot[1][-1]:.1e}")

    _, _, _, density_cool, _, temp_cool, _, _, _, _ = read_radial_profile(radialdir, fnum, simulation, "cold", weight, tail)

    print(f"Cool-phase density: {density_cool[1][-1]:.1e}")
    print(f"Cool-phase temperature: {temp_cool[1][-1]:.1e}")

if __name__ == "__main__":
    args = read_cmdline()

    basedir = args.basedir
    time = args.time
    weight = args.weight
    tail = args.tail
    simulation = args.simulation


    main(basedir, time, simulation, weight, tail)