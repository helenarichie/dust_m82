import numpy as np
import os
import sys
import pathlib
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent.resolve(), "../utils/"))
from read_cmdline import read_cmdline
from read_vertical_outflow_rates import read_vertical_outflow_rates


def main(basedir, time, simulation, field_names):
    csvdir = os.path.join(basedir, "profiles/vertical/csv/outflow_rates/")
    time_output, rates_hot, rates_mixed, rates_cool = read_vertical_outflow_rates(csvdir, field_names)

    rates_hot = np.sum(rates_hot, axis=2)
    rates_mixed = np.sum(rates_mixed, axis=2)
    rates_cool = np.sum(rates_cool, axis=2)

    cutoff = 0.01

    print(f"######### {simulation} #########")

    for i, name in enumerate(field_names):
        wh_hot = np.amin(np.where(rates_hot[i] >= cutoff))
        wh_mixed = np.amin(np.where(rates_mixed[i] >= cutoff))
        wh_cool = np.amin(np.where(rates_cool[i] >= cutoff))
        wh_time = np.where(time_output==time)[0][0]

        print(f"{name}: hot {time_output[wh_hot]/1e3} Myr, mixed {time_output[wh_mixed]/1e3} Myr, cool {time_output[wh_cool]/1e3} Myr")

        # print(f"Hot, mixed, cold at end: {rates_hot[i][wh_time]:.1f}, {rates_mixed[i][wh_time]:.1f}, {rates_cool[i][wh_time]:.1f}")
        # print(f"Total at end: {rates_hot[i][wh_time] + rates_mixed[i][wh_time] + rates_cool[i][wh_time]:.1f}")

if __name__ == "__main__":
    args = read_cmdline()

    basedir = args.basedir
    time = args.time
    simulation = args.simulation
    field_names = args.field_names

    main(basedir, time, simulation, field_names)