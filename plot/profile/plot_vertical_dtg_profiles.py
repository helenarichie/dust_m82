import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import sys
import pathlib
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent.resolve(), "../../utils/"))
from read_cmdline import read_cmdline
from read_vertical_profiles import read_vertical_profiles


def main(basedir, outdir, fig_name, field_name, time, exclude_disk, ymin, ymax, mode):
    csvdir = os.path.join(basedir, "profiles/vertical/csv/short/")

    disk_i = 0
    d_arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    if exclude_disk:
        disk_i = 1
        d_arr = d_arr[disk_i:]

    fontsize = 20
    linewidth = 3
    pad = 0.5
    labels = ["hot", "mixed", "cool"]
    color_hot, color_mixed, color_cool = sns.color_palette(palette="flare", n_colors=3)
    colors = [color_hot, color_mixed, color_cool]
    styles = ["solid", "dashed", "dashdot", "dotted"]

    ylabel = "sp"
    legend_loc = "lower left"
    legend_panel = 2
    text_x, text_y, alignment = .95, .92, "right"
    
    color = "black"
    if mode == "dark":
        plt.style.use('dark_background')
        color = "white"

    times, dust_hot, dust_mixed, dust_cool = read_vertical_profiles(csvdir, field_names)
    __annotations__, gas_hot, gas_mixed, gas_cool = read_vertical_profiles(csvdir, ["gas"])
    times = np.append(times, times[-1]+500)
    wh_time = np.where(times==time)[0][0]

    fig, ax = plt.subplots(1, len(field_names), figsize=(15, 4.5), sharey=True)

    for j, name in enumerate(field_names):
        ax[0].stairs(dust_hot[j][wh_time][disk_i:]/gas_hot[0][wh_time][disk_i:], d_arr, linestyle=styles[j], linewidth=linewidth, color=color_hot)
        ax[1].stairs(dust_mixed[j][wh_time][disk_i:]/gas_mixed[0][wh_time][disk_i:], d_arr, linestyle=styles[j], linewidth=linewidth, color=color_mixed)
        ax[2].stairs(dust_cool[j][wh_time][disk_i:]/gas_cool[0][wh_time][disk_i:], d_arr, linestyle=styles[j], linewidth=linewidth, color=color_cool)
        ax[j].tick_params(axis='both', which="both", labelsize=15, top=True, right=True)
        ax[j].set_yscale('log')
        if j == 0:
            ax[j].set_ylabel(r"$m_{dust}/m_{gas}$", fontsize=fontsize)
        ax[j].set_xlabel(r"$z~[kpc]$", fontsize=fontsize)
        ax[j].set_xlim(1-pad, np.amax(d_arr)+pad)
        ax[j].set_ylim(ymin, ymax)


        ax[2].text(text_x, text_y, r"cool", horizontalalignment=alignment, verticalalignment='center', transform = ax[2].transAxes, fontsize=fontsize-5)
        ax[0].text(text_x, text_y, r"hot", horizontalalignment=alignment, verticalalignment='center', transform = ax[0].transAxes, fontsize=fontsize-5)
        ax[1].text(text_x, text_y, r"mixed", horizontalalignment=alignment, verticalalignment='center', transform = ax[1].transAxes, fontsize=fontsize-5)


        if name.endswith("_0"):
            ax[legend_panel].plot(0, 0, linestyle=styles[j], label=r"$1~\mu$m", c=color, linewidth=linewidth)
            # ax[0].text(.05, .93, f"{round(time/1e3)} Myr", horizontalalignment='left', verticalalignment='center', transform = ax[j].transAxes, fontsize=fontsize-5)
        if name.endswith("_1"):
            ax[legend_panel].plot(0, 0, linestyle=styles[j], label=r"$0.1~\mu$m", c=color, linewidth=linewidth)
            # ax[j].text(.05, .93, r"$a=0.1~\mu$m", horizontalalignment='left', verticalalignment='center', transform = ax[j].transAxes, fontsize=fontsize-5)
        if name.endswith("_2"):
            ax[legend_panel].plot(0, 0, linestyle=styles[j], label=r"$0.01~\mu$m", c=color, linewidth=linewidth)
            # ax[j].text(.05, .93, r"$a=0.01~\mu$m", horizontalalignment='left', verticalalignment='center', transform = ax[j].transAxes, fontsize=fontsize-5)
        if name.endswith("_3"):
            ax[legend_panel].plot(0, 0, linestyle=styles[j], label=r"$0.001~\mu$m", c=color, linewidth=linewidth)
            # ax[j].text(.05, .93, r"$a=0.001~\mu$m", horizontalalignment='left', verticalalignment='center', transform = ax[j].transAxes, fontsize=fontsize-5)
    ax[legend_panel].legend(loc=legend_loc, fontsize=fontsize-5)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, f"{fig_name}.png"), dpi=300, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    args = read_cmdline()

    sys.path.insert(0, args.configdir)
    import hconfig

    basedir = args.basedir
    outdir = args.outdir
    fig_name = args.fig_name
    field_names = args.field_names
    time = args.time
    exclude_disk = args.exclude_disk
    ymin = args.ymin
    ymax = args.ymax
    mode = args.mode

    main(basedir, outdir, fig_name, field_names, time, exclude_disk, ymin, ymax, mode)