import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import sys
import pathlib
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent.resolve(), "../../utils/"))
from read_cmdline import read_cmdline
from read_vertical_outflow_rates import read_vertical_outflow_rates


def main(basedir, outdir, field_names, time, ymin, ymax, fig_name, mode):
    csvdir = os.path.join(basedir, "profiles/vertical/csv/outflow_rates/")

    time_output, rates_hot, rates_mixed, rates_cool = read_vertical_outflow_rates(csvdir, field_names)

    dt_out = time_output[1] - time_output[0]

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
    if time == -1:
        time = time_output[-1]

    time_mask = np.where(time_output <= time)

    pad = 0.1
    fontsize = 20
    linewidth = 3
    color_hot, color_mixed, color_cool = sns.color_palette(palette="flare", n_colors=3)
    styles = ["solid", "dashed", "dashdot", "dotted"]
    legend_loc = "lower left"
    legend_panel = len(field_names)-1
    text_x, text_y, alignment = .05, .92, "left"
    color = "black"
    if mode == "dark":
        plt.style.use('dark_background')
        color = "white"

    linewidth = 3
    color_hot, color_mixed, color_cool = sns.color_palette(palette="flare", n_colors=3)
    styles = ["solid", "dashed", "dashdot", "dotted"]

    line_color = "k"
    if mode == "dark":
        line_color = "white"
        plt.style.use('dark_background')

    fig, ax = plt.subplots(1, len(field_names), figsize=(15, 4.5), sharey=True)

    for i, field in enumerate(field_names):
        ax[i].semilogy(time_output[time_mask]/1e3, mass_out_hot[i][time_mask], color=color_hot, linestyle="solid", linewidth=linewidth, label="hot")
        ax[i].semilogy(time_output[time_mask]/1e3, mass_out_mixed[i][time_mask], color=color_mixed, linestyle="solid", linewidth=linewidth, label="mixed")
        ax[i].semilogy(time_output[time_mask]/1e3, mass_out_cool[i][time_mask], color=color_cool, linestyle="solid", linewidth=linewidth, label="cool")
        ax[i].semilogy(time_output[time_mask]/1e3, (mass_out_hot[i][time_mask]+mass_out_mixed[i][time_mask]+mass_out_cool[i][time_mask]), color="grey", linestyle="solid", linewidth=linewidth, label="total", alpha=0.5)

        ax[i].tick_params(axis="both", which="both", right=True, labelsize=15, top=True)
        ax[i].set_xlabel(r"$Time~[Myr]$", fontsize=fontsize)
        ax[i].set_xlim(0, time/1e3)
        ax[i].set_ylim(10, 1e5)
        
        if i == 0:
            ax[i].set_ylabel(r"${m}_{dust,out}~[M_\odot]$", fontsize=fontsize)

        # ax[i].axvline(15)

        if field.endswith("_0"):
            ax[i].text(text_x, text_y, r"$1~\mu$m", c=color, horizontalalignment=alignment, verticalalignment="center", transform=ax[i].transAxes, fontsize=fontsize-5)
        if field.endswith("_1"):
            ax[i].text(text_x, text_y, r"$0.1~\mu$m", c=color, horizontalalignment=alignment, verticalalignment="center", transform=ax[i].transAxes, fontsize=fontsize-5)
        if field.endswith("_2"):
            ax[i].text(text_x, text_y, r"$0.01~\mu$m", c=color, horizontalalignment=alignment, verticalalignment="center", transform=ax[i].transAxes, fontsize=fontsize-5)
        if field.endswith("_3"):
            ax[i].text(text_x, text_y, r"$0.001~\mu$m", c=color, horizontalalignment=alignment, verticalalignment="center", transform=ax[i].transAxes, fontsize=fontsize-5)

    ax[legend_panel].legend(loc=legend_loc, fontsize=fontsize-5)

    plt.tight_layout()
    plt.savefig(os.path.join(outdir, fig_name), dpi=300, bbox_inches="tight")

if __name__ == "__main__":
    args = read_cmdline()

    sys.path.insert(0, args.configdir)
    import hconfig

    basedir = args.basedir
    outdir = args.outdir
    mode = args.mode
    time = args.time
    ymin = args.ymin
    ymax = args.ymax
    fig_name = args.fig_name
    field_names = args.field_names

    main(basedir, outdir, field_names, time, ymin, ymax, fig_name, mode)