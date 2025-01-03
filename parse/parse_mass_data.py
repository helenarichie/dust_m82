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

    for s, field in enumerate(field_names):
        print(field)
        breakout = False
        tmax_i = 0
        masses = np.zeros((4, 10, 3))
        with open(os.path.join(csvdir, f"{field}.csv")) as f:
            for line in f:
                line = line.split(",")
                for i, bin in enumerate(line):
                    bin = bin.replace("[", "")
                    bin = bin.replace("]", "")
                    bin = bin.split(" ")
                    while("" in bin):
                        bin.remove("")
                    if i < 10:
                        masses[s][i] = np.array(bin[1:4], dtype=float)  # 1:4 = hot, mixed, cold (excludes 0, which is time)
                        time = float(bin[0])
                if time == tmaxs[tmax_i]:
                    for j in range(0, 2+1):
                        row = [tmaxs[tmax_i]]
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