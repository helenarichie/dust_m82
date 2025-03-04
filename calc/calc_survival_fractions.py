import argparse
import numpy as np
import os
from csv import writer
import sys
import pathlib
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent.resolve(), "../utils/"))
from read_cmdline import read_cmdline
from read_vertical_profiles import read_vertical_profiles
from read_vertical_outflow_rates import read_vertical_outflow_rates

def main(basedir, time, field_names, exclude_disk):

    disk_i = 0
    if exclude_disk:
        disk_i = 1

    sputtered_names = []
    for field in field_names:
        if field == "dust_0":
            sputtered_names.append("sputtered_0")
        if field == "dust_1":
            sputtered_names.append("sputtered_1")
        if field == "dust_2":
            sputtered_names.append("sputtered_2")
        if field == "dust_3":
            sputtered_names.append("sputtered_3")

    csvdir = os.path.join(basedir, "csv/short/")

    times, sputtered_hot, sputtered_mixed, sputtered_cool = read_vertical_profiles(csvdir, sputtered_names)

    csvdir = os.path.join(basedir, "csv/outflow_rates/")

    time_output, rates_hot, rates_mixed, rates_cool = read_vertical_outflow_rates(csvdir, field_names)

    dt_out = time_output[2] - time_output[1]

    mass_out_hot = []
    for rate in rates_hot:
        mass_out_i = []
        mass_cumulative = 0
        for i, rate_i in enumerate(rate):
            rate_i = np.sum(rate_i)
            mass_cumulative += rate_i * dt_out
            mass_out_i.append(mass_cumulative)
        mass_out_hot.append(mass_out_i)
    mass_out_hot = np.array(mass_out_hot)

    mass_out_mixed = []
    for rate in rates_mixed:
        mass_out_i = []
        mass_cumulative = 0
        for i, rate_i in enumerate(rate):
            rate_i = np.sum(rate_i)
            mass_cumulative += rate_i * dt_out
            mass_out_i.append(mass_cumulative)
        mass_out_mixed.append(mass_out_i)
    mass_out_mixed = np.array(mass_out_mixed)

    mass_out_cool = []
    for rate in rates_cool:
        mass_out_i = []
        mass_cumulative = 0
        for i, rate_i in enumerate(rate):
            rate_i = np.sum(rate_i)
            mass_cumulative += rate_i * dt_out
            mass_out_i.append(mass_cumulative)
        mass_out_cool.append(mass_out_i)
    mass_out_cool = np.array(mass_out_cool)

    sput_ind = np.where(times == time)[0][0]
    outflow_ind = np.where(time_output==time)[0][0]

    hot_outflow, mixed_outflow, cool_outflow = [], [], []
    hot_sput, mixed_sput, cool_sput = [], [], []
    for i, field in enumerate(field_names):
        hot_outflow.append(mass_out_hot[i][outflow_ind])
        mixed_outflow.append(mass_out_mixed[i][outflow_ind])
        cool_outflow.append(mass_out_cool[i][outflow_ind])
        hot_sput.append(np.sum(sputtered_hot[i][sput_ind][disk_i+1:]))
        mixed_sput.append(np.sum(sputtered_mixed[i][sput_ind][disk_i+1:]))
        cool_sput.append(np.sum(sputtered_cool[i][sput_ind][disk_i+1:]))

    for i, field in enumerate(field_names):
        # sputtered + outflow
        total = hot_sput[i] + mixed_sput[i] + cool_sput[i] + hot_outflow[i] + mixed_outflow[i] + cool_outflow[i]
        survived = hot_outflow[i] + mixed_outflow[i] + cool_outflow[i]
        print(f"{field} fraction: {(survived/total):.2}")


if __name__ == "__main__":
    args = read_cmdline()

    basedir = args.basedir
    time = args.time
    field_names = args.field_names
    exclude_disk = args.exclude_disk

    main(basedir, time, field_names, exclude_disk)