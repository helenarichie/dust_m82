import argparse
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import sys
import pathlib
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent.resolve(), "../utils/"))
from read_cmdline import read_cmdline
from read_radial_profile import read_radial_profile


def main(basedir, outdir, fnum, simulation, weight, tail, r_mask, mode, field_names, ymin, ymax):
    time = fnum * 50 / 1e3
    
    bin_tot, gas_hot, dust_hot, _, _, _, _, _, _, _ = read_radial_profile(basedir, fnum, simulation, "hot", weight, tail)
    _, gas_cool, dust_cool, _, _, _, _, _, _, _ = read_radial_profile(basedir ,fnum, simulation, "cold", weight, tail)

    linewidth = 2
    color_hot, color_mixed, color_cool = sns.color_palette(palette="flare", n_colors=3)
    styles = ["solid", "dashed", "dashdot", "dotted"]

    fontsize = 15
    matplotlib.rcParams.update({'font.size': fontsize})

    if mode == "dark":
        plt.style.use('dark_background')

    bin_tot = np.array(bin_tot)
    gas_hot = np.array(gas_hot)
    gas_cool = np.array(gas_cool)
    dust_hot = np.array(dust_hot)
    dust_cool = np.array(dust_cool)

    fig, ax = plt.subplots(1, 2, figsize=(10, 4), sharey=True, gridspec_kw={"wspace":0})

    for i, field in enumerate(field_names):
        ax[0].semilogy(bin_tot[bin_tot>r_mask], dust_cool[i][bin_tot>r_mask]/gas_cool[bin_tot>r_mask], linewidth=linewidth, linestyle=styles[i], color=color_cool)
        ax[1].semilogy(bin_tot[bin_tot>r_mask], dust_hot[i][bin_tot>r_mask]/gas_hot[bin_tot>r_mask], linewidth=linewidth, linestyle=styles[i], color=color_hot)

        if field == "dust_0":
            ax[1].plot(0, 0, label=r"1 $\mu$m", linestyle=styles[0], color="black", linewidth=linewidth)
        if field == "dust_1":
            ax[1].plot(0, 0, label=r"0.1 $\mu$m", linestyle=styles[1], color="black", linewidth=linewidth)
        if field == "dust_2":
            ax[1].plot(0, 0, label=r"0.01 $\mu$m", linestyle=styles[2], color="black", linewidth=linewidth)
        if field == "dust_3": 
            ax[1].plot(0, 0, label=r"0.001 $\mu$m", linestyle=styles[3], color="black", linewidth=linewidth)
    
    ax[1].legend(fontsize=fontsize-2)
    ax[1].set_xticks([2, 4, 6, 8, 10])

    for ax_i in ax:
        ax_i.set_ylim(ymin, ymax)
        ax_i.set_xlim(0, 10)
        ax_i.set_xlabel("r [kpc]")
        ax_i.tick_params(axis='both', which="both", labelsize=fontsize-2, top=True, right=True)
    
    ax[0].set_ylabel(r"$m_{dust}/m_{gas}$")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, f"{simulation}_dgr_profile{tail}.png"), dpi=300)
    plt.close()

if __name__ == "__main__":
    args = read_cmdline()

    sys.path.insert(0, args.configdir)
    import hconfig

    basedir = args.basedir
    outdir = args.outdir
    fnum = args.fnum
    simulation = args.simulation
    weight = args.weight
    tail = args.tail
    r_mask = args.rmask
    mode = args.mode
    field_names = args.field_names
    ymin = args.ymin
    ymax = args.ymax

    main(basedir, outdir, fnum, simulation, weight, tail, r_mask, mode, field_names, ymin, ymax)
