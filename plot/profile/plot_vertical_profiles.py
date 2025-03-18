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


def main(basedir, outdir, fig_name, field_names, time, exclude_disk, ymin, ymax, mode):
    csvdir = os.path.join(basedir, "profiles/vertical/csv/short/")

    norm = True

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

    if field_names[0].startswith("sputtered"):
        ylabel = "sp"
        legend_loc = "upper left"
        legend_panel = 2
        text_x, text_y, alignment = .95, .92, "right"
    if field_names[0].startswith("dust"):
        ylabel = "dust"
        legend_loc = "upper right"
        legend_panel = 0
        text_x, text_y, alignment = .05, .92, "left"
    if field_names[0].startswith("gas"):
        ylabel = "gas"
        legend_loc = "upper right"
        legend_panel = 2
        text_x, text_y, alignment = .05, .92, "left"
    
    color = "black"
    if mode == "dark":
        plt.style.use('dark_background')
        color = "white"

    times, mass_hot, mass_mixed, mass_cool = read_vertical_profiles(csvdir, field_names)
    times = np.append(times, times[-1]+500)
    wh_time = np.where(times==time)[0][0]

    fig, ax = plt.subplots(1, len(field_names), figsize=(15, 4.5), sharey=True)

    for j, name in enumerate(field_names):
        if not norm:
            ax[0].stairs(mass_hot[j][wh_time][disk_i:], d_arr, linestyle=styles[j], linewidth=linewidth, color=color_hot)
            ax[1].stairs(mass_mixed[j][wh_time][disk_i:], d_arr, linestyle=styles[j], linewidth=linewidth, color=color_mixed)
            ax[2].stairs(mass_cool[j][wh_time][disk_i:], d_arr, linestyle=styles[j], linewidth=linewidth, color=color_cool)
            y_ax_label = r"$m_{{{:s}}}~[M_\odot]$".format(ylabel)
        else:
            ax[0].stairs(mass_hot[j][wh_time][disk_i:]/mass_hot[j][wh_time][0], d_arr, linestyle=styles[j], linewidth=linewidth, color=color_hot)
            ax[1].stairs(mass_mixed[j][wh_time][disk_i:]/mass_hot[j][wh_time][0], d_arr, linestyle=styles[j], linewidth=linewidth, color=color_mixed)
            ax[2].stairs(mass_cool[j][wh_time][disk_i:]/mass_hot[j][wh_time][0], d_arr, linestyle=styles[j], linewidth=linewidth, color=color_cool)
            y_ax_label = r"$m_{{{:s}}}/m_{{disk}}$".format(ylabel)
        ax[j].tick_params(axis='both', which="both", labelsize=15, top=True, right=True)
        ax[j].set_yscale('log')
        if j == 0:
            ax[j].set_ylabel(y_ax_label, fontsize=fontsize)
        ax[j].set_xlabel(r"$z~[kpc]$", fontsize=fontsize)
        ax[j].set_xlim(1-pad, np.amax(d_arr)+pad)
        ax[j].set_ylim(ymin, ymax)

        if name.endswith("_0"):
            ax[legend_panel].plot(0, 0, linestyle=styles[j], label=r"$1~\mu$m", c=color, linewidth=linewidth)
        if name.endswith("_1"):
            ax[legend_panel].plot(0, 0, linestyle=styles[j], label=r"$0.1~\mu$m", c=color, linewidth=linewidth)
        if name.endswith("_2"):
            ax[legend_panel].plot(0, 0, linestyle=styles[j], label=r"$0.01~\mu$m", c=color, linewidth=linewidth)
        if name.endswith("_3"):
            ax[legend_panel].plot(0, 0, linestyle=styles[j], label=r"$0.001~\mu$m", c=color, linewidth=linewidth)

    if field_names[0].startswith("dust"):
        ax[2].text(.95, .92, r"cool", horizontalalignment="right", verticalalignment='center', transform = ax[2].transAxes, fontsize=fontsize-5)
    else:
        ax[2].text(text_x, text_y, r"cool", horizontalalignment=alignment, verticalalignment='center', transform = ax[2].transAxes, fontsize=fontsize-5)
    ax[0].text(text_x, text_y, r"hot", horizontalalignment=alignment, verticalalignment='center', transform = ax[0].transAxes, fontsize=fontsize-5)
    ax[1].text(text_x, text_y, r"mixed", horizontalalignment=alignment, verticalalignment='center', transform = ax[1].transAxes, fontsize=fontsize-5)
    
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