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
    p.add_argument("-o", "--outdir", type=str, required=True)
    p.add_argument("-n", "--fig-name", type=str, required=True)
    p.add_argument('-t', '--tmax', type=float, required=False, default=-1)
    p.add_argument("-l", "--ymin", type=float, required=False, default=-1)
    p.add_argument("-u", "--ymax", type=float, required=False, default=-1)
    p.add_argument("-m", "--mode", type=str, choices=["dark", "light"], required=False, default="light")
    p.add_argument('-f', '--field-names', nargs="+", default=[])
    args = p.parse_args()
    return args

def main(basedir, outdir, field_names, tmax, ymin, ymax, fig_name, mode):
    csvdir = os.path.join(basedir, "csv/old/")

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
    
    # plot outflow rates
    if tmax == -1:
        tmax = time_output[-1]

    time_mask = np.where(time_output <= tmax)

    if ymin == -1:
        ymin = None
    if ymax == -1:
        ymax = None

    xmin = np.amin(time_output[time_mask]/1e3)
    xmax = np.amax(time_output[time_mask]/1e3)

    linewidth = 3
    color_hot, color_mixed, color_cool = sns.color_palette(palette="flare", n_colors=3)
    styles = ["solid", "dashed", "dashdot", "dotted"]

    line_color = "k"
    if mode == "dark":
        line_color = "white"
        plt.style.use('dark_background')

    fig, ax = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

    for i, grain in enumerate(field_names):
        ax[0].plot(time_output[time_mask]/1e3, mass_out_hot[i][time_mask], linestyle=styles[i], linewidth=linewidth, c=color_hot)
    ax[0].tick_params(axis='both', which="both", labelsize=15, top=True, right=True)
    ax[0].set_yscale('log')
    ax[0].set_ylabel(r"$m_{out}~[M_\odot]$", fontsize=20)
    ax[0].set_xlabel(r"$t~[Myr]$", fontsize=20)
    ax[0].set_xlim(xmin, xmax)
    ax[0].set_ylim(ymin, ymax)
    # ax[0].vlines(30, ymin=ymin, ymax=ymax, linewidth=linewidth-0.5, zorder=0, color="lightgrey", alpha=0.7)

    for i, grain in enumerate(field_names):
        ax[1].plot(time_output[time_mask]/1e3, mass_out_mixed[i][time_mask], linestyle=styles[i], linewidth=linewidth, c=color_mixed)
    ax[1].tick_params(axis='both', which="both", labelsize=15, top=True, right=True)
    ax[1].set_yscale('log')
    ax[1].set_xlabel(r"$t~[Myr]$", fontsize=20)
    ax[1].set_xlim(xmin, xmax)
    ax[1].set_ylim(ymin, ymax)
    # ax[1].vlines(30, ymin=ymin, ymax=ymax, linewidth=linewidth-0.5, zorder=0, color="lightgrey", alpha=0.7)

    for i, grain in enumerate(field_names):
        ax[2].plot(time_output[time_mask]/1e3, mass_out_cool[i][time_mask], linestyle=styles[i], linewidth=linewidth, c=color_cool)
    ax[2].tick_params(axis='both', which="both", labelsize=15, top=True, right=True)
    ax[2].set_yscale('log')
    ax[2].set_xlabel(r"$t~[Myr]$", fontsize=20)
    ax[2].set_xlim(xmin, xmax)
    ax[2].set_ylim(ymin, ymax)
    # ax[2].vlines(30, ymin=ymin, ymax=ymax, linewidth=linewidth-0.5, zorder=0, color="lightgrey", alpha=0.7)
    for i, name in enumerate(field_names):
        if name == "dust_0":
            ax[2].plot(0, 0, linestyle=styles[i], label=r"$a=1~\mu$m", c=line_color, linewidth=linewidth)
        if name == "dust_1":
            ax[2].plot(0, 0, linestyle=styles[i], label=r"$a=0.1~\mu$m", c=line_color, linewidth=linewidth)
        if name == "dust_2":
            ax[2].plot(0, 0, linestyle=styles[i], label=r"$a=0.01~\mu$m", c=line_color, linewidth=linewidth)
        if name == "dust_3":
            ax[2].plot(0, 0, linestyle=styles[i], label=r"$a=0.001~\mu$m", c=line_color, linewidth=linewidth)
    ax[2].legend(fontsize=15, loc="upper left")

    plt.tight_layout()
    plt.savefig(outdir + f"mass_out_{fig_name}.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    args = read_cmdline()

    sys.path.insert(0, args.configdir)
    import hconfig

    basedir = args.basedir
    outdir = args.outdir
    mode = args.mode
    tmax = args.tmax
    ymin = args.ymin
    ymax = args.ymax
    fig_name = args.fig_name
    field_names = args.field_names

    main(basedir, outdir, field_names, tmax, ymin, ymax, fig_name, mode)