import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import sys
import pathlib
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent.resolve(), "../../utils/"))
from read_cmdline import read_cmdline
from read_vertical_outflow_rates import read_vertical_outflow_rates

def main(basedir, outdir, fig_name, field_names, time, ymin, ymax, mode):
    csvdir = os.path.join(basedir, "profiles/vertical/csv/outflow_rates/")
    time_output, rates_hot, rates_mixed, rates_cool = read_vertical_outflow_rates(csvdir, field_names)

    rates_hot = np.sum(rates_hot, axis=2)
    rates_mixed = np.sum(rates_mixed, axis=2)
    rates_cool = np.sum(rates_cool, axis=2)

    wh_time = np.where(time_output == time)[0][0]

    fontsize = 20
    linewidth = 3
    color_hot, color_mixed, color_cool = sns.color_palette(palette="flare", n_colors=3)
    styles = ["solid", "dashed", "dashdot", "dotted"]
    legend_loc = "upper right"
    legend_panel = len(field_names)-1
    text_x, text_y, alignment = .05, .92, "left"
    color = "black"
    if mode == "dark":
        plt.style.use('dark_background')
        color = "white"

    fig, ax = plt.subplots(1, len(field_names), figsize=(15, 4.5), sharey=True)

    for i, field in enumerate(field_names):
        
        ax[i].plot(time_output[:wh_time]/1e3, rates_hot[i][:wh_time], color=color_hot, linestyle="solid", linewidth=linewidth, label="hot")
        ax[i].plot(time_output[:wh_time]/1e3, rates_mixed[i][:wh_time], color=color_mixed, linestyle="solid", linewidth=linewidth, label="mixed")
        ax[i].plot(time_output[:wh_time]/1e3, rates_cool[i][:wh_time], color=color_cool, linestyle="solid", linewidth=linewidth, label="cool")

        ax[i].tick_params(axis="both", which="both", labelsize=15, top=True, right=True)
        ax[i].set_xlabel(r"$Time~[Myr]$", fontsize=fontsize)
        ax[i].set_xlim(0, time/1e3)
        ax[i].set_ylim(ymin, ymax)

        if field.endswith("_0"):
            ax[i].text(text_x, text_y, r"$1~\mu$m", c=color, horizontalalignment=alignment, verticalalignment="center", transform=ax[i].transAxes, fontsize=fontsize-5)
        if field.endswith("_1"):
            ax[i].text(text_x, text_y, r"$0.1~\mu$m", c=color, horizontalalignment=alignment, verticalalignment="center", transform=ax[i].transAxes, fontsize=fontsize-5)
        if field.endswith("_2"):
            ax[i].text(text_x, text_y, r"$0.01~\mu$m", c=color, horizontalalignment=alignment, verticalalignment="center", transform=ax[i].transAxes, fontsize=fontsize-5)
        if field.endswith("_3"):
            ax[i].text(text_x, text_y, r"$0.001~\mu$m", c=color, horizontalalignment=alignment, verticalalignment="center", transform=ax[i].transAxes, fontsize=fontsize-5)
    
    ax[0].set_ylabel(r"$\dot{m}_{dust}~[M_\odot\,yr^{-1}]$", fontsize=fontsize)

    ax[legend_panel].legend(loc=legend_loc, fontsize=fontsize-5)

    plt.tight_layout()
    plt.savefig(os.path.join(outdir, fig_name), dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    args = read_cmdline()

    sys.path.insert(0, args.configdir)
    import hconfig

    basedir = args.basedir
    outdir = args.outdir
    fig_name = args.fig_name
    field_names = args.field_names
    time = args.time
    ymin = args.ymin
    ymax = args.ymax
    mode = args.mode

    main(basedir, outdir, fig_name, field_names, time, ymin, ymax, mode)
