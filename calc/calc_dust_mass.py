import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import sys
import pathlib
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent.resolve(), "../utils/"))
from read_vertical_profiles import read_vertical_profiles
from read_cmdline import read_cmdline

def main(basedir, field_names, time):

    sputtered_names = ["sputtered_0", "sputtered_1", "sputtered_2", "sputtered_3"]

    csvdir = os.path.join(basedir, "csv/")
        
    times, mass_hot, mass_mixed, mass_cool = read_vertical_profiles(csvdir, field_names)
    _, sputtered_hot, sputtered_mixed, sputtered_cool = read_vertical_profiles(csvdir, sputtered_names[0:len(field_names)]) 

    wh_time = np.where(times==time)[0][0]

    for n, name in enumerate(field_names):

        initial_mass = np.sum(sputtered_cool[n][0][:])+np.sum(sputtered_mixed[n][0][:])+np.sum(sputtered_hot[n][0][:])+np.sum(mass_cool[n][0][:])+np.sum(mass_mixed[n][0][:])+np.sum(mass_hot[n][0][:])

        print(f"\n########################### {time/1e3} Myr ###############################")
        sputtered_hot_time, sputtered_mixed_time, sputtered_cool_time = np.sum(sputtered_hot[n][wh_time][:]), np.sum(sputtered_mixed[n][wh_time][:]), np.sum(sputtered_cool[n][wh_time][:])
        mass_hot_time, mass_mixed_time, mass_cool_time = np.sum(mass_hot[n][wh_time][:]), np.sum(mass_mixed[n][wh_time][:]), np.sum(mass_cool[n][wh_time][:])
        total_sputtered_time = sputtered_hot_time + sputtered_mixed_time + sputtered_cool_time
        total_mass_time = mass_hot_time + mass_mixed_time + mass_cool_time

        print(f"\nHot {name} sputtered: {sputtered_hot_time/initial_mass:.3e}")
        print(f"Mixed {name} sputtered: {sputtered_mixed_time/initial_mass:.3e}")
        print(f"Cool {name} sputtered: {sputtered_cool_time/initial_mass:.3e}")
        print(f"Total {name} sputtered: {(sputtered_hot_time+sputtered_mixed_time+sputtered_cool_time)/initial_mass:.3e}")

        print(f"Initial-(current+sputtered) {name} mass: {(initial_mass-(total_sputtered_time+total_mass_time)):.3e} M_sun")

if __name__ == "__main__":
    args = read_cmdline()

    basedir = args.basedir
    field_names = args.field_names
    time = args.sim_time

    main(basedir, field_names, time)