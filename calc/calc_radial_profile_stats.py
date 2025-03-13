import numpy as np
import os
import sys
import pathlib
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent.resolve(), "../utils/"))
from read_cmdline import read_cmdline
from read_radial_profile import read_radial_profile
from calc_tau_sp import calc_tau_sp


def main(basedir, time, simulation, weight, tail):
    radialdir = os.path.join(basedir, "profiles/radial/")

    radius = 5

    print(f"######### {simulation} #########")

    fnum = int(time * 2 / 100)
    bin_tot, _, _, density_hot, _, temp_hot, _, _, _, _ = read_radial_profile(radialdir, fnum, simulation, "hot", weight, tail)
    bin_tot = np.array(bin_tot)
    wh_rad = np.argmin(abs(bin_tot - radius))

    print(f"Hot-phase density: {density_hot[1][wh_rad]:.1e}")
    print(f"Hot-phase temperature: {temp_hot[1][wh_rad]:.1e}")
    print(f"Hot-phase sputtering time: {calc_tau_sp(density_hot[1][wh_rad], temp_hot[1][wh_rad], 1)/1e6:.1e} Myr")

    bin_tot, _, _, density_cool, _, temp_cool, _, _, _, _ = read_radial_profile(radialdir, fnum, simulation, "cold", weight, tail)

    print(f"Cool-phase density: {density_cool[1][wh_rad]:.1e}")
    print(f"Cool-phase temperature: {temp_cool[1][wh_rad]:.1e}")
    print(f"Cool-phase sputtering time: {calc_tau_sp(density_cool[1][wh_rad], temp_cool[1][wh_rad], 1)/1e6:.1e} Myr")

if __name__ == "__main__":
    args = read_cmdline()

    basedir = args.basedir
    time = args.time
    weight = args.weight
    tail = args.tail
    simulation = args.simulation


    main(basedir, time, simulation, weight, tail)