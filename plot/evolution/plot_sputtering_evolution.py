import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import sys
import pathlib
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent.resolve(), "../utils/"))
from read_vertical_profiles import read_vertical_profiles
from read_cmdline import read_cmdline

def main(basedir, outdir, field_names, exclude_disk, ymax, mode, tmax, simulation):
    disk_i = 0

    csvdir = os.path.join(basedir, "profiles/vertical/csv/")

    fontsize = 15

    if exclude_disk:
        disk_i = 1

    color_hot, color_mixed, color_cool = sns.color_palette(palette="flare", n_colors=3)
    styles = ["solid", "dashed", "dashdot", "dotted"]

    dust_names = ["dust_0", "dust_1", "dust_2", "dust_3"]

    if mode == "dark":
        plt.style.use('dark_background')

    times, sputtered_hot, sputtered_mixed, sputtered_cool = read_vertical_profiles(csvdir, field_names)
    _, mass_hot, mass_mixed, mass_cool = read_vertical_profiles(csvdir, dust_names[0:len(field_names)])

    times = np.append(times, times[-1]+500)

    fig, ax = plt.subplots(1, 3, figsize=(16, 5), sharey=False)
    ymin = 1
    linewidth = 3
    # disk_i + 1 because the 0th index is the simulation time
    for j, grain in enumerate(field_names):
        ax[0].plot(times/1e3, sputtered_hot[j][:,0], linestyle=styles[j], linewidth=linewidth-1, color="k")
        ax[0].plot(times/1e3, mass_hot[j][:,0], linestyle=styles[j], linewidth=linewidth, color=color_hot)
    ax[0].tick_params(axis='both', which="both", labelsize=15, top=True, right=True)
    ax[0].set_yscale('log')
    ax[0].set_ylabel(r"$m_{dust}~[M_\odot]$", fontsize=fontsize)
    ax[0].set_xlabel(r"$Time~[Myr]$", fontsize=fontsize)
    ax[0].set_xlim(np.amin(times/1e3), tmax)
    ax[0].set_ylim(ymin, None)

    for j, grain in enumerate(field_names):
        ax[1].plot(times/1e3, sputtered_mixed[j][:,0], linestyle=styles[j], linewidth=linewidth-1, color="k")
        ax[1].plot(times/1e3, mass_mixed[j][:,0], linestyle=styles[j], linewidth=linewidth, color=color_mixed)
    ax[1].tick_params(axis='both', which="both", labelsize=15, top=True, right=True)
    ax[1].set_yscale('log')
    ax[1].set_xlabel(r"$Time~[Myr]$", fontsize=fontsize)
    ax[1].set_xlim(np.amin(times/1e3), tmax)
    ax[1].set_ylim(ymin, None)


    ax[0].plot(0, 0, linestyle="solid", label=r"sputtered", c="k", linewidth=linewidth-1)
    ax[1].plot(0, 0, linestyle="solid", label=r"sputtered", c="k", linewidth=linewidth-1)
    ax[2].plot(0, 0, linestyle="solid", label=r"sputtered", c="k", linewidth=linewidth-1)
    ax[0].plot(0, 0, linestyle="solid", label=r"total", c=color_hot, linewidth=linewidth)
    ax[1].plot(0, 0, linestyle="solid", label=r"total", c=color_mixed, linewidth=linewidth)
    ax[2].plot(0, 0, linestyle="solid", label=r"total", c=color_cool, linewidth=linewidth)

    ax[0].legend(fontsize=fontsize-2, loc="lower right")
    ax[1].legend(fontsize=fontsize-2, loc="lower right")
    ax[2].legend(fontsize=fontsize-2, loc="lower right")

    for j, grain in enumerate(field_names):
        ax[2].plot(times/1e3, sputtered_cool[j][:,0], linestyle=styles[j], linewidth=linewidth-1, color="k")
        ax[2].plot(times/1e3, mass_cool[j][:,0], linestyle=styles[j], linewidth=linewidth, color=color_cool)
    ax[2].tick_params(axis='both', which="both", labelsize=15, top=True, right=True)
    ax[2].set_yscale('log')
    ax[2].set_xlabel(r"$Time~[Myr]$", fontsize=fontsize)
    ax[2].set_xlim(np.amin(times/1e3), tmax)
    ax[2].set_ylim(ymin, None)

    ax[0].text(.05, .93, r"hot", horizontalalignment='left', verticalalignment='center', transform = ax[0].transAxes, fontsize=fontsize-2)
    ax[1].text(.05, .93, r"mixed", horizontalalignment='left', verticalalignment='center', transform = ax[1].transAxes, fontsize=fontsize-2)
    ax[2].text(.05, .05, r"cool", horizontalalignment='left', verticalalignment='center', transform = ax[2].transAxes, fontsize=fontsize-2)

    plt.tight_layout()
    plt.savefig(os.path.join(outdir, f"{simulation}_sputtering_evolution.png"), dpi=300)
    plt.close()

if __name__ == "__main__":
    args = read_cmdline()

    sys.path.insert(0, args.configdir)
    import hconfig

    basedir = args.basedir
    outdir = args.outdir
    field_names = args.field_names
    exclude_disk = args.exclude_disk
    ymax = args.ymax
    mode = args.mode
    tmax = args.tmax
    simulation = args.simulation

    main(basedir, outdir, field_names, exclude_disk, ymax, mode, tmax, simulation)