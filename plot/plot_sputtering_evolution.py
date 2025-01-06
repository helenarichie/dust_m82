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
    p.add_argument("-e", "--exclude_disk", type=bool, required=False, default=True)
    p.add_argument("-y", "--ymax", type=float, required=False, default=1e5)
    p.add_argument("-m", "--mode", type=str, choices=["dark", "light"], required=False, default="light")
    p.add_argument('-f', '--field-names', nargs="+", default=[])
    args = p.parse_args()
    return args

def main(basedir, field_names, exclude_disk, ymax, mode):
    disk_i = 0

    csvdir = os.path.join(basedir, "csv/")

    if exclude_disk:
        disk_i = 1

    color_hot, color_mixed, color_cool = sns.color_palette(palette="flare", n_colors=3)
    colors = [color_hot, color_mixed, color_cool]
    styles = ["solid", "dashdot", "dotted", "dashed"]

    if mode == "dark":
        plt.style.use('dark_background')

    times = None
    sputtered_hot = []
    for field in field_names:
        times = []
        sputtered_i = []
        with open(os.path.join(csvdir, f"{field}_hot_short.csv")) as f:
            for line in f:
                line = line.split(",")
                # disk_i + 1 because the 0th index is the time
                sputtered_i.append(np.sum(np.array(line[disk_i+1:], dtype=float)))
                times.append(float(line[0]))
        sputtered_hot.append(sputtered_i)
    sputtered_hot = np.array(sputtered_hot)
    times = np.array(times)

    sputtered_mixed = []
    for field in field_names:
        sputtered_i = []
        with open(os.path.join(csvdir, f"{field}_mixed_short.csv")) as f:
            for line in f:
                line = line.split(",")
                sputtered_i.append(np.sum(np.array(line[disk_i+1:], dtype=float)))
        sputtered_mixed.append(sputtered_i)
    sputtered_mixed = np.array(sputtered_mixed)

    sputtered_cool = []
    for field in field_names:
        sputtered_i = []
        with open(os.path.join(csvdir, f"{field}_cool_short.csv")) as f:
            for line in f:
                line = line.split(",")
                sputtered_i.append(np.sum(np.array(line[disk_i+1:], dtype=float)))
        sputtered_cool.append(sputtered_i)
    sputtered_cool = np.array(sputtered_cool)

    fig, ax = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
    ymin = 1
    linewidth = 3
    # disk_i + 1 because the 0th index is the simulation time
    for j, grain in enumerate(field_names):
        ax[0].plot(times/1e3, sputtered_hot[j], linestyle=styles[j], linewidth=linewidth, color=color_hot)
    ax[0].tick_params(axis='both', which="both", labelsize=15, top=True, right=True)
    ax[0].set_yscale('log')
    ax[0].set_ylabel(r"$m_{sput}~[M_\odot]$", fontsize=20)
    ax[0].set_xlabel(r"$Time~[Myr]$", fontsize=20)
    ax[0].set_xlim(np.amin(times/1e3), np.amax(times/1e3))
    ax[0].set_ylim(ymin, ymax)

    for j, grain in enumerate(field_names):
        ax[1].plot(times/1e3, sputtered_mixed[j], linestyle=styles[j], linewidth=linewidth, color=color_mixed)
    ax[1].tick_params(axis='both', which="both", labelsize=15, top=True, right=True)
    ax[1].set_yscale('log')
    ax[1].set_xlabel(r"$Time~[Myr]$", fontsize=20)
    ax[1].set_xlim(np.amin(times/1e3), np.amax(times/1e3))
    ax[1].set_ylim(ymin, ymax)

    for j, name in enumerate(field_names):
        if name == "sputtered_0":
            ax[2].plot(0, 0, linestyle=styles[j], label=r"$a=1~\mu$m", c="k", linewidth=linewidth)
        if name == "sputtered_1":
            ax[2].plot(0, 0, linestyle=styles[j], label=r"$a=0.1~\mu$m", c="k", linewidth=linewidth)
        if name == "sputtered_2":
            ax[2].plot(0, 0, linestyle=styles[j], label=r"$a=0.01~\mu$m", c="k", linewidth=linewidth)
        if name == "sputtered_3":
            ax[2].plot(0, 0, linestyle=styles[j], label=r"$a=0.001~\mu$m", c="k", linewidth=linewidth)
    ax[2].legend(fontsize=15, loc="upper left")

    for j, grain in enumerate(field_names):
        ax[2].plot(times/1e3, sputtered_cool[j], linestyle=styles[j], linewidth=linewidth, color=color_cool)
    ax[2].tick_params(axis='both', which="both", labelsize=15, top=True, right=True)
    ax[2].set_yscale('log')
    ax[2].set_xlabel(r"$Time~[Myr]$", fontsize=20)
    ax[2].set_xlim(np.amin(times/1e3), np.amax(times/1e3))
    ax[2].set_ylim(ymin, ymax)

    plt.tight_layout()
    plt.savefig(os.path.join(basedir, "png", "sputtering_evolution.png"), dpi=300)
    plt.close()

if __name__ == "__main__":
    args = read_cmdline()

    sys.path.insert(0, args.configdir)
    import hconfig

    basedir = args.basedir
    field_names = args.field_names
    exclude_disk = args.exclude_disk
    ymax = args.ymax
    mode = args.mode

    main(basedir, field_names, exclude_disk, ymax, mode)