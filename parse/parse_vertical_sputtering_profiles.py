import argparse
import numpy as np
import os
from csv import writer

def read_cmdline():
    p = argparse.ArgumentParser()
    p.add_argument("-b", "--basedir", type=str, required=True)
    args = p.parse_args()
    return args

def main(basedir):
    fields = ["sputtered_0", "sputtered_1", "sputtered_2", "sputtered_3"]
    labels = ["hot", "mixed", "cool"]
    tmaxs = np.linspace(0, 50000, 101)

    csvdir = basedir

    for field in fields:
        f = open(os.path.join(csvdir, f"{field}_hot_short.csv"), "w")
        f.close()
        f = open(os.path.join(csvdir, f"{field}_mixed_short.csv"), "w")
        f.close()
        f = open(os.path.join(csvdir, f"{field}_cool_short.csv"), "w")
        f.close()

    for s, field in enumerate(fields):
        print(field)
        breakout = False
        tmax_i = 0
        sputtered = np.zeros((4, 10, 3))
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
                        sputtered[s][i] = sputtered[s][i] + np.array(bin[1:4], dtype=float)
                        time = float(bin[0])
                if time == tmaxs[tmax_i]:
                    for j in range(0, 2+1):
                        row = [tmaxs[tmax_i]]
                        for sput in sputtered[s][:,j]:
                            row.append(sput)
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

    main(basedir)