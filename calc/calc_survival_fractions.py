import argparse
import numpy as np
import os
from csv import writer

def read_cmdline():
    p = argparse.ArgumentParser()
    p.add_argument("-b", "--basedir", type=str, required=True)
    p.add_argument('-t', '--time', type=float, required=True)
    p.add_argument('-f', '--field-names', nargs="+", default=[])
    p.add_argument('-e', '--exclude-disk', type=bool, default=False)
    args = p.parse_args()
    return args

def main(basedir, time, field_names, exclude_disk):

    disk_i = 0
    if exclude_disk:
        disk_i = 1

    csvdir = os.path.join(basedir, "csv/")

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

    sputtered_hot = []
    sputtered_mixed = []
    sputtered_cool = []

    for name in sputtered_names:
        sputtered_i = []
        with open(os.path.join(csvdir, f"{name}_hot_short.csv"), "r") as f:
            for line in f:
                line = line.rstrip("\n")
                line = line.split(",")
                sputtered_i.append(line)
        f.close()
        sputtered_hot.append(sputtered_i)
    sputtered_hot = np.array(sputtered_hot, dtype=float)

    for name in sputtered_names:
        sputtered_i = []
        with open(os.path.join(csvdir, f"{name}_mixed_short.csv"), "r") as f:
            for line in f:
                line = line.rstrip("\n")
                line = line.split(",")
                sputtered_i.append(line)
        f.close()
        sputtered_mixed.append(sputtered_i)
    sputtered_mixed = np.array(sputtered_mixed, dtype=float)

    for name in sputtered_names:
        sputtered_i = []
        with open(os.path.join(csvdir, f"{name}_cool_short.csv"), "r") as f:
            for line in f:
                line = line.rstrip("\n")
                line = line.split(",")
                sputtered_i.append(line)
        f.close()
        sputtered_cool.append(sputtered_i)
    sputtered_cool = np.array(sputtered_cool, dtype=float)

    rates_hot = []
    for field in field_names:
        rate_i = []
        with open(os.path.join(csvdir, f"rate_{field}_hot_1e-24.csv")) as f:
            for line in f:
                line = line.split(",")
                rate_i.append(np.array(line, dtype=float))
        rates_hot.append(rate_i)

    rates_mixed = []
    for field in field_names:
        rate_i = []
        with open(os.path.join(csvdir, f"rate_{field}_mixed_1e-24.csv")) as f:
            for line in f:
                line = line.split(",")
                rate_i.append(np.array(line, dtype=float))
        rates_mixed.append(rate_i)

    rates_cool = []
    for field in field_names:
        rate_i = []
        with open(os.path.join(csvdir, f"rate_{field}_cool_1e-24.csv")) as f:
            for line in f:
                line = line.split(",")
                rate_i.append(np.array(line, dtype=float))
        rates_cool.append(rate_i)

    time_output = []
    with open(os.path.join(csvdir, "time_output_1e-24.csv")) as f:
        for line in f:
            time_output.append(float(line))
    time_output = np.array(time_output)

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

    sput_ind = np.where(sputtered_cool[0,:,0]==time)[0][0]
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