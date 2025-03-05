import argparse
import numpy as np
import os
import sys
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent.resolve(), "../utils/"))
from read_cmdline import read_cmdline
from csv import writer


def main(basedir, outdir, log_name, field):

    if field == "Sputtered":
        field_names = ["sputtered_0", "sputtered_1", "sputtered_2", "sputtered_3"]
    if field == "Dust":
        field_names = ["dust_0", "dust_1", "dust_2", "dust_3"]
    if field == "Gas":
        field_names = ["gas"]

    for name in field_names:
        f = open(os.path.join(outdir, f"{name}.csv"), "w")
        f.close()
    f = open(os.path.join(outdir, f"{field.lower()}_time.csv"), "w")
    f.close()

    time = 0

    N_bins = 10

    rows = np.zeros((len(field_names), N_bins, 3))

    with open(os.path.join(basedir, f"{log_name}.log")) as f:
        for line in f:
            line_split = list(line)
            if line.startswith("n_step"):
                line_temp = line.split(" ")
                while("" in line_temp):
                    line_temp.remove("")
                time = float(line_temp[4])
                with open(os.path.join(outdir, f"{field.lower()}_time.csv"), "a") as f_txt:
                    writer_obj = writer(f_txt)
                    writer_obj.writerow([time])
                    f_txt.close()
                for n, name in enumerate(field_names):
                    with open(os.path.join(outdir, f"{name}.csv"), "a") as f_txt:
                        writer_obj = writer(f_txt)
                        writer_obj.writerow(rows[n])
                        f_txt.close()
                if field != "Sputtered":
                    rows = np.zeros((len(field_names), N_bins, 3))
            elif line_split[0].isdigit() and line_split[1] == " ":
                if line_split[3] == field[0]:
                    line = line.replace(f"{field} mass:  (hot) ", "")
                    line = line.replace("(mixed) ", "")
                    line = line.replace("(cool) ", "")
                    line.rstrip("\n")
                    line = line.split("  ")
                    while("" in line):
                        line.remove("")
                    # for each vertical bin
                    for i in range(0, N_bins):
                        # if i is the bin index
                        if line[0] == str(i):
                            for n, name in enumerate(field_names):
                                if field == "Sputtered":
                                    rows[n][i] += np.array([float(line[n+1]), float(line[n+5]), float(line[n+9])])
                                if field == "Dust":
                                    rows[n][i] = np.array([float(line[n+1]), float(line[n+5]), float(line[n+9])])
                                if field == "Gas":
                                    rows[n][i] = np.array([float(line[n+1]), float(line[n+2]), float(line[n+3])])

if __name__ == "__main__":
    args = read_cmdline()

    basedir = args.basedir
    outdir = args.outdir
    log_name = args.log_name
    field_name = args.field_name

    main(basedir, outdir, log_name, field_name)