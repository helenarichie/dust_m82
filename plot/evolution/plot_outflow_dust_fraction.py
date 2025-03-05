import numpy as np
import os
import seaborn as sns
import sys
import pathlib
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent.resolve(), "../utils/"))
from read_cmdline import read_cmdline
from read_vertical_profiles import read_vertical_profiles

def main(basedir, outdir, field_names, time, simulation):
    datadir = os.path.join(basedir, "profiles/vertical/csv/")
    times, mass_hot, mass_mixed, mass_cool = read_vertical_profiles(datadir, field_names)
    color_hot, color_mixed, color_cool = sns.color_palette(palette="flare", n_colors=3)
    linewidth = 2
    fontsize = 15
    styles = ["solid", "dashed", "dotted"]

    fig, ax = plt.subplots(1, len(field_names), figsize=(16, 5), sharey=False)

    times = np.append(times, 50e3)

    for i, name in enumerate(field_names):
        ax[0].plot(times[times<=time]/1e3, np.sum(mass_hot[i][times<=time,1:], axis=1)/mass_hot[i][times<=time,0], color=color_hot, linestyle=styles[i], linewidth=linewidth)
        ax[1].plot(times[times<=time]/1e3, np.sum(mass_mixed[i][times<=time,1:], axis=1)/mass_mixed[i][times<=time,0], color=color_mixed, linestyle=styles[i], linewidth=linewidth)
        ax[2].plot(times[times<=time]/1e3, np.sum(mass_cool[i][times<=time,1:], axis=1)/mass_cool[i][times<=time,0], color=color_cool, linestyle=styles[i], linewidth=linewidth)
        ax[i].set_xlabel("Time [Myr]", fontsize=fontsize)
        ax[i].tick_params(axis='both', which="both", labelsize=fontsize-2, top=True, right=True)
        ax[i].set_xlim(0, time/1e3)

        if name == "dust_0":
            ax[0].plot(0, 0, label=r"1 $\mu$m", linestyle=styles[0], color="black", linewidth=linewidth)
        if name == "dust_1":
            ax[0].plot(0, 0, label=r"0.1 $\mu$m", linestyle=styles[1], color="black", linewidth=linewidth)
        if name == "dust_2":
            ax[0].plot(0, 0, label=r"0.01 $\mu$m", linestyle=styles[2], color="black", linewidth=linewidth)
        if name == "dust_3": 
            ax[0].plot(0, 0, label=r"0.001 $\mu$m", linestyle=styles[3], color="black", linewidth=linewidth)

    ax[0].set_ylabel(r"$m_{dust,z>1 kpc}/m_{dust,z<1 kpc}$", fontsize=fontsize)
    ax[0].legend(fontsize=fontsize-2)

    plt.tight_layout()
    plt.savefig(os.path.join(outdir, f"{simulation}_outflow_mass_fraction.png"), dpi=300)


if __name__ == "__main__":
    args = read_cmdline()

    sys.path.insert(0, args.configdir)
    import hconfig
    
    basedir = args.basedir
    outdir = args.outdir
    field_names = args.field_names
    time = args.sim_time
    simulation = args.simulation

    main(basedir, outdir, field_names, time, simulation)