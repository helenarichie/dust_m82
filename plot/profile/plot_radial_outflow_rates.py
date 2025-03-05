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
    p.add_argument("-f", "--fnum", type=int, required=True)
    p.add_argument("-s", "--simulation", type=str, required=True)
    p.add_argument("-t", "--tail", type=str, required=False, default="")
    p.add_argument("-r", "--rmask", type=int, required=False, default=0)
    p.add_argument("-l", "--ymin", type=float, required=False, default=-1)
    p.add_argument("-u", "--ymax", type=float, required=False, default=-1)
    p.add_argument("-m", "--mode", type=str, choices=["dark", "light"], required=False, default="light")
    p.add_argument('-n', '--field-names', nargs="+", default=[])
    args = p.parse_args()
    return args

def main(basedir, outdir, fnum, simulation, tail, r_mask, ymin, ymax, mode, field_names):
    N_bins = 80
    r_mask = 0
    time = fnum * 50 / 1e3
    fontsize = 15

    if ymin == -1:
        ymin = None
    if ymax == -1:
        ymax = None

    f_name = f"{fnum}_prof_{simulation}_outflow{tail}.txt"

    bins = []
    gas_rate_hot = []
    momentum_rate_hot = []
    energy_rate_hot = []
    gas_rate_mixed = []
    momentum_rate_mixed = []
    energy_rate_mixed = []
    gas_rate_cool = []
    momentum_rate_cool = []
    energy_rate_cool = []
    dust_0_rate_hot = []
    dust_0_rate_mixed = []
    dust_0_rate_cool = []
    dust_1_rate_hot = []
    dust_1_rate_mixed = []
    dust_1_rate_cool = []
    dust_2_rate_hot = []
    dust_2_rate_mixed = []
    dust_2_rate_cool = []
    dust_3_rate_hot = []
    dust_3_rate_mixed = []
    dust_3_rate_cool = []

    parse = False

    with open(os.path.join(basedir, f_name)) as f:
        line_i = 0
        for line in f:
            if parse:
                line_i += 1
                line = line.strip(" ").rstrip("\n").split(",")
                bins.append(float(line[0]))
                # hot
                gas_rate_hot.append(float(line[2]))
                momentum_rate_hot.append(float(line[3]))
                energy_rate_hot.append(float(line[4]))
                # mixed
                gas_rate_mixed.append(float(line[6]))
                momentum_rate_mixed.append(float(line[7]))
                energy_rate_mixed.append(float(line[8]))
                # cool
                gas_rate_cool.append(float(line[10]))
                momentum_rate_cool.append(float(line[11]))
                energy_rate_cool.append(float(line[12]))
                # dust_0
                dust_0_rate_hot.append(float(line[13]))
                dust_0_rate_mixed.append(float(line[14]))
                dust_0_rate_cool.append(float(line[15]))
                # dust_1
                dust_1_rate_hot.append(float(line[16]))
                dust_1_rate_mixed.append(float(line[17]))
                dust_1_rate_cool.append(float(line[18]))
                # dust_2
                dust_2_rate_hot.append(float(line[19]))
                dust_2_rate_mixed.append(float(line[20]))
                dust_2_rate_cool.append(float(line[21]))
                # dust_3
                dust_3_rate_hot.append(float(line[22]))
                dust_3_rate_mixed.append(float(line[23]))
                dust_3_rate_cool.append(float(line[24]))
            elif line.startswith("# Radial bin"):
                parse = True

    bins = np.array(bins)
    gas_rate_hot = np.array(gas_rate_hot)
    gas_rate_mixed = np.array(gas_rate_mixed)
    gas_rate_cool = np.array(gas_rate_cool)
    energy_rate_hot = np.array(energy_rate_hot)
    energy_rate_mixed = np.array(energy_rate_mixed)
    energy_rate_cool = np.array(energy_rate_cool)
    momentum_rate_hot = np.array(momentum_rate_hot)
    momentum_rate_mixed = np.array(momentum_rate_mixed)
    momentum_rate_cool = np.array(momentum_rate_cool)

    dust_rate_hot = np.array([dust_0_rate_hot, dust_1_rate_hot, dust_2_rate_hot, dust_3_rate_hot], dtype=float)
    dust_rate_mixed = np.array([dust_0_rate_mixed, dust_1_rate_mixed, dust_2_rate_mixed, dust_3_rate_mixed], dtype=float)
    dust_rate_cool = np.array([dust_0_rate_cool, dust_1_rate_cool, dust_2_rate_cool, dust_3_rate_cool], dtype=float)

    gas_color = "mediumturquoise"
    energy_color = "mediumorchid"
    momentum_color = "palevioletred"
    linewidth = 2
    hot_style = "solid"
    mixed_style = "dashed"
    cool_style = "dashdot"

    cool_color = "cornflowerblue"
    mixed_color = "mediumseagreen"
    hot_color = "red"
    tot_color = "black"

    if mode == "dark":
        plt.style.use('dark_background')

    fig, ax = plt.subplots(3, 1, figsize=(5, 10), sharex=True)

    # *1e-3 converts rate from per kyr to per year
    ax[0].plot(bins[bins>r_mask], gas_rate_hot[bins>r_mask] * 1e-3, c=hot_color, linewidth=linewidth, label="hot")
    ax[0].plot(bins[bins>r_mask], gas_rate_mixed[bins>r_mask] * 1e-3, c=mixed_color, linewidth=linewidth, label="mixed")
    ax[0].plot(bins[bins>r_mask], gas_rate_cool[bins>r_mask] * 1e-3, c=cool_color, linewidth=linewidth, label="cool")
    ax[0].plot(bins[bins>r_mask], (gas_rate_cool[bins>r_mask]+gas_rate_mixed[bins>r_mask]+gas_rate_hot[bins>r_mask]) * 1e-3, c=tot_color, linewidth=linewidth, label="tot")
    # ax[0].set_title(rf"${round(time, 1)}$ Myr", fontsize=fontsize)
    ax[0].set_ylabel(r"$\dot{m}_{gas}$ $[M_\odot\,yr^{-1}]$", fontsize=fontsize)
    ax[0].legend()
    ax[0].tick_params(axis='both', which="both", top=True, right=True, labelsize=fontsize-3)
    ax[0].set_xlim(np.amin(bins[bins>r_mask]), np.amax(bins[bins>r_mask]))

    # M_sun * kpc / kyr^-2 to M_sun * km / s / yr
    momentum_conversion = (3.086e+16 / 3.154e+10) * 1e-3
    ax[1].plot(bins[bins>r_mask], momentum_rate_hot[bins>r_mask] * momentum_conversion, c=hot_color, linewidth=linewidth, label="hot")
    ax[1].plot(bins[bins>r_mask], momentum_rate_mixed[bins>r_mask] * momentum_conversion, c=mixed_color, linewidth=linewidth, label="mixed")
    ax[1].plot(bins[bins>r_mask], momentum_rate_cool[bins>r_mask] * momentum_conversion, c=cool_color, linewidth=linewidth, label="cool")
    ax[1].plot(bins[bins>r_mask], (momentum_rate_cool[bins>r_mask]+momentum_rate_mixed[bins>r_mask]+momentum_rate_hot[bins>r_mask]) * momentum_conversion, c=tot_color, linewidth=linewidth, label="tot")
    ax[1].set_ylabel(r"$\dot{p}$ $[M_\odot\,km\,s^{-1}\,yr^{-1}]$", fontsize=fontsize)
    ax[1].tick_params(axis='both', which="both", top=True, right=True, labelsize=fontsize-3)
    ax[1].set_xlim(np.amin(bins[bins>r_mask]), np.amax(bins[bins>r_mask]))

    # M_sun * kpc^2 / kyr^3 to erg / s
    energy_conversion = 3.154e-10 * (1.99e33 * (3.09e21)**2 * (3.154e10)**-2)
    ax[2].semilogy(bins[bins>r_mask], energy_rate_hot[bins>r_mask] * energy_conversion, c=hot_color, linewidth=linewidth, label="hot")
    ax[2].semilogy(bins[bins>r_mask], energy_rate_mixed[bins>r_mask] * energy_conversion, c=mixed_color, linewidth=linewidth, label="mixed")
    ax[2].semilogy(bins[bins>r_mask], energy_rate_cool[bins>r_mask] * energy_conversion, c=cool_color, linewidth=linewidth, label="cool")
    ax[2].semilogy(bins[bins>r_mask], (energy_rate_cool[bins>r_mask]+energy_rate_mixed[bins>r_mask]+energy_rate_hot[bins>r_mask]) * energy_conversion, c=tot_color, linewidth=linewidth, label="tot")
    ax[2].set_ylabel(r"$\dot{E}$ $[erg\,s^{-1}]$", fontsize=fontsize)
    ax[2].set_xlabel("r [kpc]", fontsize=fontsize)
    ax[2].tick_params(axis='both', which="both", top=True, right=True, labelsize=fontsize-3)
    ax[2].set_xlim(np.amin(bins[bins>r_mask]), np.amax(bins[bins>r_mask]))
 
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, f"{simulation}_{fnum}_gas_outflow{tail}.png"), dpi=300)
    plt.close()

    fig, ax = plt.subplots(1, 1, figsize=(5.5, 5))

    # *1e-3 converts rate from per kyr to per year
    ax.plot(bins[bins>r_mask], gas_rate_hot[bins>r_mask] * 1e-3, c=hot_color, linewidth=linewidth, label="hot")
    ax.plot(bins[bins>r_mask], gas_rate_mixed[bins>r_mask] * 1e-3, c=mixed_color, linewidth=linewidth, label="mixed")
    ax.plot(bins[bins>r_mask], gas_rate_cool[bins>r_mask] * 1e-3, c=cool_color, linewidth=linewidth, label="cool")
    ax.plot(bins[bins>r_mask], (gas_rate_cool[bins>r_mask]+gas_rate_mixed[bins>r_mask]+gas_rate_hot[bins>r_mask]) * 1e-3, c=tot_color, linewidth=linewidth, label="tot")
    # ax[0].set_title(rf"${round(time, 1)}$ Myr", fontsize=fontsize)
    ax.set_ylabel(r"$\dot{m}_{gas}$ $[M_\odot\,yr^{-1}]$", fontsize=fontsize)
    ax.legend()
    ax.tick_params(axis='both', which="both", top=True, right=True, labelsize=fontsize-3)
    ax.set_xlim(np.amin(bins[bins>r_mask]), np.amax(bins[bins>r_mask]))
    ax.set_ylim(0, 7.5)
    ax.set_xlabel("r [kpc]", fontsize=fontsize)
 
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, f"{simulation}_gas_outflow_rate{tail}.png"), dpi=300)
    plt.close()

    fig, ax = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

    ax[0].tick_params(axis='both', which="both", top=True, right=True, labelsize=fontsize-3)
    ax[0].set_xlim(np.amin(bins[bins>r_mask]), np.amax(bins[bins>r_mask]))
    ax[0].set_ylim(ymin, ymax)
    # ax[0].text(0.75, 0.0145, rf"${round(time, 1)}$ Myr", fontsize=fontsize-3)
    ax[0].set_xlabel("r [kpc]", fontsize=fontsize)
    ax[0].set_ylabel(r"$\dot{m}_{dust}$ $[M_\odot\,yr^{-1}]$", fontsize=fontsize)
    ax[1].set_xlabel("r [kpc]", fontsize=fontsize)
    ax[1].tick_params(axis='both', which="both", top=True, right=True, labelsize=fontsize-3)
    ax[1].set_xlim(np.amin(bins[bins>r_mask]), np.amax(bins[bins>r_mask]))
    ax[2].tick_params(axis='both', which="both", top=True, right=True, labelsize=fontsize-3)
    ax[2].set_xlim(np.amin(bins[bins>r_mask]), np.amax(bins[bins>r_mask]))
    ax[2].set_xlabel("r [kpc]", fontsize=fontsize)

    color_hot, color_mixed, color_cool = sns.color_palette(palette="flare", n_colors=3)
    styles = ["solid", "dashed", "dashdot", "dotted"]
    labels = [r"$1~\mu$m", r"$0.1~\mu$m", r"$0.01~\mu$m"]

    for i, field in enumerate(field_names):
        if field == "dust_0":
            ax[2].plot(0, 0, linestyle=styles[0], label=r"$a=1~\mu$m", c="k", linewidth=linewidth)
        if field == "dust_1":
            ax[2].plot(0, 0, linestyle=styles[1], label=r"$a=0.1~\mu$m", c="k", linewidth=linewidth)
        if field == "dust_2":
            ax[2].plot(0, 0, linestyle=styles[2], label=r"$a=0.01~\mu$m", c="k", linewidth=linewidth)
        if field == "dust_3":
           ax[2].plot(0, 0, linestyle=styles[3], label=r"$a=0.001~\mu$m", c="k", linewidth=linewidth)

        # *1e-3 converts rate from per kyr to per year
        ax[i].plot(bins[bins>r_mask], dust_rate_hot[i][bins>r_mask] * 1e-3, c=color_hot, linewidth=linewidth, linestyle=styles[i])
        ax[i].plot(bins[bins>r_mask], dust_rate_mixed[i][bins>r_mask] * 1e-3, c=color_mixed, linewidth=linewidth, linestyle=styles[i])
        ax[i].plot(bins[bins>r_mask], dust_rate_cool[i][bins>r_mask] * 1e-3, c=color_cool, linewidth=linewidth, linestyle=styles[i])
        ax[i].plot(bins[bins>r_mask], (dust_rate_cool[i][bins>r_mask]+dust_rate_mixed[i][bins>r_mask]+dust_rate_hot[i][bins>r_mask]) * 1e-3, c="k", linewidth=linewidth, linestyle=styles[i])
        ax[i].text(.95, .93, f"{labels[i]}", horizontalalignment='right', verticalalignment='center', transform = ax[i].transAxes, fontsize=fontsize-3)
    
    # ax[2].legend()

    # plt.suptitle(rf"${round(time, 1)}$ Myr", fontsize=fontsize, y=0.95)

    plt.tight_layout()
    plt.savefig(os.path.join(outdir, f"{simulation}_{fnum}_dust_outflow_rate{tail}.png"), dpi=300)
    plt.close()

if __name__ == "__main__":
    args = read_cmdline()

    sys.path.insert(0, args.configdir)
    import hconfig

    basedir = args.basedir
    outdir = args.outdir
    fnum = args.fnum
    simulation = args.simulation
    tail = args.tail
    r_mask = args.rmask
    mode = args.mode
    ymin = args.ymin
    ymax = args.ymax
    field_names = args.field_names

    main(basedir, outdir, fnum, simulation, tail, r_mask, ymin, ymax, mode, field_names)