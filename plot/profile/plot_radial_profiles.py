import argparse
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import sys
import pathlib
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent.resolve(), "../../utils/"))
from read_cmdline import read_cmdline
from read_radial_profile import read_radial_profile


def main(basedir, outdir, fnum, simulation, phase, weight, tail, r_mask, mode):

    radial_dir = os.path.join(basedir, "profiles/radial/")

    bin_tot, m_gas, m_dust, density, cell_count, temperature, velocity, pressure, entropy, mach = read_radial_profile(radial_dir, fnum, simulation, phase, weight, tail)

    linewidth = 2
    color_hot, color_mixed, color_cool = sns.color_palette(palette="flare", n_colors=3)
    styles = ["solid", "dashed", "dashdot", "dotted"]
    if phase == "hot":
        color = color_hot
    if phase == "mixed":
        color = color_mixed
    if phase == "cold":
        color = color_cool

    matplotlib.rcParams.update({'font.size': 15})

    if mode == "dark":
        plt.style.use('dark_background')

    bin_tot = np.array(bin_tot)

    def n_hot(r, n1):
        return n1 * r ** (-0.05 * r - 1.08)
    def n_cold(r, n1):
        return n1 * r ** -2
    
    fig, ax = plt.subplots(2, 3, figsize=(15, 7.5), sharex=True)

    ax[0][0].semilogy(bin_tot, density[0], c=color, label="avg", linewidth=linewidth)
    ax[0][0].semilogy(bin_tot, density[1], c=color, label="med", linestyle="--", linewidth=linewidth)
    ax[0][0].fill_between(bin_tot, density[2], density[3], color=color, alpha=0.2)

    lopez_densities = [1.6, 0.8, 4.9, 3.7, 23, 7.9, 5.2, 5.1, 8.4, 4.6, 3.3, 2.6, 3.4, 2.6]  # cm^-3
    lopez_density_err = [0.1, 0.1, 0.2, 0.2, 0.4, 0.2, 0.3, 0.1, 0.15, 0.14, 0.1, 0.2, 0.2, 0.2]  # cm^-3
    lopez_distance = [2.08, 2.57, 0.88, 0.76, 0.48, 0.60, 0.69, 1.16, 1.05, 1.73, 1.69, 1.94, 1.87, 1.82]  # kpc

    if phase == "hot":
        ax[0][0].plot(bin_tot, n_hot(bin_tot, density[1][np.where(bin_tot==1)[0][0]]), linewidth=linewidth, label=r"$n\propto r^f$, $f=−0.05r−1.08$", c="k")
    if phase == "cold":
        ax[0][0].plot(bin_tot, n_cold(bin_tot, density[1][np.where(bin_tot==1)[0][0]]), linewidth=linewidth, label=r"$n\propto r^{-2}$", c="k")
        ax[0][0].errorbar(lopez_distance, lopez_densities, yerr=lopez_density_err, fmt="x", c="k", elinewidth=1, label="Lopez+2025")
    ax[0][0].legend(fontsize=13)
    ax[0][0].set_ylabel(r"$n_{gas}$ $[cm^{-3}]$")

    ax[0][1].semilogy(bin_tot, velocity[0], c=color, linewidth=linewidth)
    ax[0][1].semilogy(bin_tot, velocity[1], c=color, linestyle="--", linewidth=linewidth)
    ax[0][1].fill_between(bin_tot, velocity[2], velocity[3], color=color, alpha=0.2)
    ax[0][1].set_ylabel(r"$v_{r}$ $[km\,s^{-1}]$")

    ax[0][2].plot(bin_tot, np.log10(pressure[0]), c=color, label="avg", linewidth=linewidth)
    ax[0][2].plot(bin_tot, np.log10(pressure[1]), c=color, label="med", linestyle="--", linewidth=linewidth)
    ax[0][2].fill_between(bin_tot, np.log10(pressure[2]), np.log10(pressure[3]), color=color, alpha=0.2)
    ax[0][2].set_ylabel(r"$P/k_B~[K~cm^{-3}]$")

    ax[1][0].plot(bin_tot, np.log10(temperature[0]), c=color, label="avg", linewidth=linewidth)
    ax[1][0].plot(bin_tot, np.log10(temperature[1]), c=color, label="med", linestyle="--", linewidth=linewidth)
    ax[1][0].fill_between(bin_tot, np.log10(temperature[2]), np.log10(temperature[3]), color=color, alpha=0.2)
    ax[1][0].set_xlabel("r [kpc]")
    ax[1][0].set_ylabel(r"$\log(T_{gas}$ $[K]$)")

    ax[1][1].plot(bin_tot, mach[0], c=color, label="avg", linewidth=linewidth)
    ax[1][1].plot(bin_tot, mach[1], c=color, label="med", linestyle="--", linewidth=linewidth)
    ax[1][1].fill_between(bin_tot, mach[2], mach[3], color=color, alpha=0.2)
    ax[1][1].set_xlabel("r [kpc]")
    ax[1][1].set_ylabel(r"$M$")

    ax[1][2].semilogy(bin_tot, entropy[0], c=color, label="avg", linewidth=linewidth)
    ax[1][2].semilogy(bin_tot, entropy[1], c=color, label="med", linestyle="--", linewidth=linewidth)
    ax[1][2].fill_between(bin_tot, entropy[2], entropy[3], color=color, alpha=0.2)
    ax[1][2].set_xlabel("r [kpc]")
    ax[1][2].set_ylabel(r"$S/k_B~[K\,cm^{-3}]$")
    
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, f"{simulation}_{fnum}_{phase}_{weight}{tail}.png"), dpi=300)
    plt.close()


if __name__ == "__main__":
    args = read_cmdline()

    sys.path.insert(0, args.configdir)
    import hconfig

    basedir = args.basedir
    outdir = args.outdir
    fnum = args.fnum
    simulation = args.simulation
    phase = args.phase
    weight = args.weight
    tail = args.tail
    r_mask = args.rmask
    mode = args.mode

    main(basedir, outdir, fnum, simulation, phase, weight, tail, r_mask, mode)
