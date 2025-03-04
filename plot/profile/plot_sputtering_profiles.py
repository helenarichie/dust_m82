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

def main(basedir, outdir, fig_name, field_names, exclude_disk, ymin, ymax, mode):
    disk_i = 0

    csvdir = os.path.join(basedir, "csv/")

    d_arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    if exclude_disk:
        disk_i = 1
        d_arr = d_arr[disk_i:]

    color_hot, color_mixed, color_cool = sns.color_palette(palette="flare", n_colors=3)
    colors = [color_hot, color_mixed, color_cool]
    styles = ["solid", "dashed", "dashdot", "dotted"]
    dust_names = ["dust_0", "dust_1", "dust_2", "dust_3"]

    fontsize = 20
    linewidth = 3
    pad = 0.5
    sputtered_color = "black"

    if mode == "dark":
        plt.style.use('dark_background')
        sputtered_color = "white"

    times, sputtered_hot, sputtered_mixed, sputtered_cool = read_vertical_profiles(csvdir, field_names)
    _, mass_hot, mass_mixed, mass_cool = read_vertical_profiles(csvdir, dust_names[0:len(field_names)])

    times = np.append(times, times[-1]+500)


    for i, time in enumerate(times):

        fig, ax = plt.subplots(1, len(field_names), figsize=(15, 5), sharey=True)

        for j, grain in enumerate(field_names):
            ax[0].stairs(sputtered_hot[j][i][disk_i:], d_arr, linestyle=styles[j], linewidth=linewidth-1, color=sputtered_color)
            ax[1].stairs(sputtered_mixed[j][i][disk_i:], d_arr, linestyle=styles[j], linewidth=linewidth-1, color=sputtered_color)
            ax[2].stairs(sputtered_cool[j][i][disk_i:], d_arr, linestyle=styles[j], linewidth=linewidth-1, color=sputtered_color)
            ax[0].stairs(mass_hot[j][i][disk_i:], d_arr, linestyle=styles[j], linewidth=linewidth, color=color_hot)
            ax[1].stairs(mass_mixed[j][i][disk_i:], d_arr, linestyle=styles[j], linewidth=linewidth, color=color_mixed)
            ax[2].stairs(mass_cool[j][i][disk_i:], d_arr, linestyle=styles[j], linewidth=linewidth, color=color_cool)
            ax[j].tick_params(axis='both', which="both", labelsize=15, top=True, right=True)
            ax[j].set_yscale('log')
            if j == 0:
                ax[j].set_ylabel(r"$m_{dust}~[M_\odot]$", fontsize=fontsize)
            ax[j].set_xlabel(r"$z~[kpc]$", fontsize=fontsize)
            ax[j].set_xlim(1-pad, np.amax(d_arr)+pad)
            ax[j].set_ylim(ymin, ymax)

        """
        for j, name in enumerate(field_names):
            if name == "sputtered_0":
                ax[2].plot(0, 0, linestyle=styles[j], label=r"$1~\mu$m", c=sputtered_color, linewidth=linewidth)
                ax[0].text(.05, .93, f"{round(time/1e3)} Myr", horizontalalignment='left', verticalalignment='center', transform = ax[j].transAxes, fontsize=fontsize-5)
            if name == "sputtered_1":
                ax[2].plot(0, 0, linestyle=styles[j], label=r"$0.1~\mu$m", c=sputtered_color, linewidth=linewidth)
                # ax[j].text(.05, .93, r"$a=0.1~\mu$m", horizontalalignment='left', verticalalignment='center', transform = ax[j].transAxes, fontsize=fontsize-5)
            if name == "sputtered_2":
                ax[2].plot(0, 0, linestyle=styles[j], label=r"$0.01~\mu$m", c=sputtered_color, linewidth=linewidth)
                # ax[j].text(.05, .93, r"$a=0.01~\mu$m", horizontalalignment='left', verticalalignment='center', transform = ax[j].transAxes, fontsize=fontsize-5)
            if name == "sputtered_3":
                ax[2].plot(0, 0, linestyle=styles[j], label=r"$0.001~\mu$m", c=sputtered_color, linewidth=linewidth)
                # ax[j].text(.05, .93, r"$a=0.001~\mu$m", horizontalalignment='left', verticalalignment='center', transform = ax[j].transAxes, fontsize=fontsize-5)
        """

        ax[2].text(.05, .93, r"cool", horizontalalignment='left', verticalalignment='center', transform = ax[2].transAxes, fontsize=fontsize-5)
        ax[0].text(.05, .93, r"hot", horizontalalignment='left', verticalalignment='center', transform = ax[0].transAxes, fontsize=fontsize-5)
        ax[1].text(.05, .93, r"mixed", horizontalalignment='left', verticalalignment='center', transform = ax[1].transAxes, fontsize=fontsize-5)

        ax[2].plot(0, 0, linestyle="solid", label=r"total", c=color_cool, linewidth=linewidth)
        ax[2].plot(0, 0, linestyle="solid", label=r"sputtered", c=sputtered_color, linewidth=linewidth-1)
        ax[2].legend(fontsize=fontsize-5, loc="upper right")

        ax[1].plot(0, 0, linestyle="solid", label=r"total", c=color_mixed, linewidth=linewidth)
        ax[1].plot(0, 0, linestyle="solid", label=r"sputtered", c=sputtered_color, linewidth=linewidth-1)
        ax[1].legend(fontsize=fontsize-5, loc="upper right")

        ax[0].plot(0, 0, linestyle="solid", label=r"total", c=color_hot, linewidth=linewidth)
        ax[0].plot(0, 0, linestyle="solid", label=r"sputtered", c=sputtered_color, linewidth=linewidth-1)
        ax[0].legend(fontsize=fontsize-5, loc="upper right")
    
        plt.tight_layout()
        plt.savefig(os.path.join(outdir, f"{fig_name}{int(time/500)}_{mode}.png"), dpi=300)
        plt.close()


if __name__ == "__main__":
    args = read_cmdline()

    sys.path.insert(0, args.configdir)
    import hconfig

    basedir = args.basedir
    outdir = args.outdir
    fig_name = args.fig_name
    field_names = args.field_names
    exclude_disk = args.exclude_disk
    ymin = args.ymin
    ymax = args.ymax
    mode = args.mode

    main(basedir, outdir, fig_name, field_names, exclude_disk, ymin, ymax, mode)