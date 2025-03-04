import argparse
import numpy as np
import os
from csv import writer

def read_cmdline():
    p = argparse.ArgumentParser()
    p.add_argument("-b", "--basedir", type=str, required=True)
    p.add_argument('-f', '--field-names', nargs="+", default=[])
    args = p.parse_args()
    return args

def main(basedir, field_names):
    labels = ["hot", "mixed", "cool"]
    tmaxs = np.linspace(0, 50000, 101)

    csvdir = basedir

    for field in field_names:
        f = open(os.path.join(csvdir, f"{field}_hot_short.csv"), "w")
        f.close()
        f = open(os.path.join(csvdir, f"{field}_mixed_short.csv"), "w")
        f.close()
        f = open(os.path.join(csvdir, f"{field}_cool_short.csv"), "w")
        f.close()
    f = open(os.path.join(csvdir, f"time_short.csv"), "w")
    f.close()

    times = [0]
    with open(os.path.join(csvdir, f"{field_names[0].split('_')[0]}_time.csv"), "r") as f:
        for line in f:
            times.append(float(line))

    for s, field in enumerate(field_names):
        print(field)
        breakout = False
        tmax_i = 0
        masses = np.zeros((4, 10, 3))
        with open(os.path.join(csvdir, f"{field}.csv")) as f:
            for l, line in enumerate(f):
                line = line.split(",")
                for i, bin in enumerate(line):
                    bin = bin.replace("[", "")
                    bin = bin.replace("]", "")
                    bin = bin.split(" ")
                    while("" in bin):
                        bin.remove("")
                    if i < 10:
                        masses[s][i] = np.array(bin[0:3], dtype=float)  # 0:3 = hot, mixed, cold
                        time = times[l]
                if time == tmaxs[tmax_i]:
                    if s == 0 and time != 0:
                        with open(os.path.join(csvdir, f"time_short.csv"), "a") as f_write:
                            writer_obj = writer(f_write)
                            writer_obj.writerow([time])
                            f_write.close()
                    for j in range(0, 2+1):
                        row = []
                        for mass in masses[s][:,j]:
                            row.append(mass)
                        with open(os.path.join(csvdir, f"{field}_{labels[j]}_short.csv"), "a") as f_write:
                            writer_obj = writer(f_write)
                            writer_obj.writerow(row)
                            f_write.close()
                    if tmax_i < (len(tmaxs)-1):
                        tmax_i += 1
                    else:
                        breakout = True
                        break
                if breakout:
                    break

if __name__ == "__main__":
    args = read_cmdline()

    basedir = args.basedir
    field_names = args.field_names

    main(basedir, field_names)