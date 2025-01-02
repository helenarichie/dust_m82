import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import sys

def read_cmdline():
    p = argparse.ArgumentParser()
    p.add_argument("-b", "--basedir", type=str, required=True)
    p.add_argument("-c", "--configdir", type=str, required=True)
    p.add_argument("-f", "--field_name", type=str, required=True)
    p.add_argument("-e", "--exclude_disk", type=bool, required=False, default=True)
    p.add_argument("-y", "--ymax", type=float, required=False, default=5e8)
    p.add_argument("-m", "--mode", type=str, choices=["dark", "light"], required=False, default="light")
    args = p.parse_args()
    return args

def main(basedir, field_name, exclude_disk, ymax, mode):
    tmaxs = np.linspace(0, 50000, 101)
    disk_i = 0

    csvdir = os.path.join(basedir, "csv/")

    d_arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    if exclude_disk:
        disk_i = 1
        d_arr = d_arr[disk_i:]

    sputtered = np.zeros((10, 3))

    labels = ["hot", "mixed", "cool"]
    color_hot, color_mixed, color_cool = sns.color_palette(palette="flare", n_colors=3)
    colors = [color_hot, color_mixed, color_cool]

    if mode == "dark":
        plt.style.use('dark_background')

    breakout = False
    tmax_i = 0
    with open(os.path.join(csvdir, f"{field_name}.csv")) as f:
        for line in f:
            line = line.split(",")
            for i, bin in enumerate(line):
                bin = bin.replace("[", "")
                bin = bin.replace("]", "")
                bin = bin.split(" ")
                while("" in bin):
                    bin.remove("")
                if i < 10:
                    sputtered[i] = sputtered[i] + np.array(bin[1:4], dtype=float)
                if float(bin[0]) == tmaxs[tmax_i]:
                    for j, color in enumerate(colors):
                        plt.stairs(sputtered[:,j][1:], d_arr, color=color, label=labels[j] + rf", total = {np.sum(sputtered[:,j][1:]):.1e} $M_\odot$", linewidth=2, zorder=-j)
                        print(f"{labels[j]} {field_name} total mass at {round(tmaxs[tmax_i]/1e3, 1):.2e} Myr: {np.sum(sputtered[:,j][1:]):.2e} M_sun")
                    print("\n")
                    plt.title(f"cumulative {field_name} mass, $t={round(tmaxs[tmax_i]/1e3, 1)}$ Myr")
                    plt.yscale('log')
                    plt.ylabel(r"$log_{10}(M~[M_\odot])$")
                    plt.xlabel(r"$r~[kpc]$")
                    plt.ylim(1, ymax)
                    plt.legend()
                    plt.savefig(os.path.join(basedir, "png", field_name, f"{int(tmaxs[tmax_i]/500)}_{field_name}.png"), dpi=300)
                    plt.close()

                    if tmax_i < (len(tmaxs)-1):
                        tmax_i += 1
                    else:
                        breakout = True
                        break
            if breakout:
                break

if __name__ == "__main__":
    args = read_cmdline()

    sys.path.insert(0, args.configdir)
    import hconfig

    basedir = args.basedir
    exclude_disk = args.field_name
    field_name = args.field_name
    ymax = args.ymax
    mode = args.mode

    main(basedir, field_name, exclude_disk, ymax, mode)