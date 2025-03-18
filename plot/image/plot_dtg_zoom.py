import argparse
import h5py
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import os
import seaborn as sns
import sys

def read_cmdline():
    p = argparse.ArgumentParser()
    p.add_argument("-b", "--basedir", type=str, required=True)
    p.add_argument("-c", "--configdir", type=str, required=True)
    p.add_argument('-f', '--field-names', nargs="+", default=[])
    p.add_argument("-s", "--nstart", type=int, required=True)
    p.add_argument("-e", "--nend", type=int, required=True)
    p.add_argument("-d", "--slice", type=str, choices=["xz", "xy"], required=False, default="xz")
    p.add_argument("-m", "--mode", type=str, choices=["dark", "light"], required=False, default="light")
    p.add_argument("-l", "--cbar-lower", type=float, required=False, default=0)
    p.add_argument("-u", "--cbar-upper", type=float, required=False, default=0.01)
    
    args = p.parse_args()
    return args
    
def main(basedir, field_names, ns, ne, vmin, vmax, slice, mode):
    # define data directories
    datadir = os.path.join(basedir, "hdf5", "slice")
    pngdir = os.path.join(basedir, "png", "dtg")

    # set plotting style
    if mode == "dark":
        plt.style.use('dark_background')

    # cmap = sns.cubehelix_palette(start=.2, rot=-.3, as_cmap=True, reverse=True)
    cmap = sns.color_palette("cubehelix", as_cmap=True)
    matplotlib.rcParams.update({'font.size': 14})
    clabel = r'$\rho_{dust}/\rho_{gas}$'

    time_x, time_y = 8, 19
    sbar_x, sbar_y = 2, 1
    linewidth = 2
    panel_width = 2.5
    cbar_width = 0.3
    fig_width = len(field_names) * panel_width + cbar_width
    cbar_gridspec = (panel_width + cbar_width) / panel_width
    labels = [r"$1~\mu$m", r"$0.1~\mu$m", r"$0.01~\mu$m"]

    width_ratios = []
    for i in field_names:
        width_ratios.append(1)
    # width_ratios[-1] = cbar_gridspec

    # define physical constants
    mu = 0.6 # mean molecular weight
    MP = 1.672622e-24 # proton mass, g
    KB = 1.380658e-16 # Boltzmann constant, cm^2 g s^-2 K^-1

    for fnum in range(ns, ne+1):
        f = h5py.File(os.path.join(datadir, str(fnum)+"_slice.h5"), "r")
        
        head = f.attrs
        dx = head["dx"][0]
        t = head["t"][0]
        gamma = head["gamma"][0]
        nx, ny, nz = head["dims"][0], head["dims"][1], head["dims"][2]
        dx = head["dx"][0]

        width = 1024
        x_start = 2150
        x_end = x_start + width
        # y_start = 1550
        y_start = 300
        y_end = y_start + int(width/2)
    
        if slice == "xz":
            xlen = (width)*dx
            ylen = int(width/2)*dx
            aspect = nz / nx
        if slice == "xy":
            xlen = nx*dx
            ylen = ny*dx
            aspect = ny / nx
        gas_density = np.array(f[f"d_{slice}"])

        spacing = xlen/6
        sbar_label = f"{spacing:.1f} kpc"

        xticks = np.arange(0, xlen, spacing)
        yticks = np.arange(0, ylen, spacing)

        fig, ax = plt.subplots(len(field_names), 1, figsize=((aspect * panel_width)+(aspect * panel_width)*0.1, fig_width), gridspec_kw={"wspace":0, "hspace":0})
        panel_height = (aspect * panel_width)
        total_height = (aspect * panel_width)+(aspect * panel_width)*0.1
        if len(field_names) == 1:
            ax = [ax]

        if len(field_names) != 1:
            for ax_i in ax:
                for child in ax_i.get_children():
                    if isinstance(child, matplotlib.spines.Spine):
                        child.set_color("white")

        for i, field_i in enumerate(field_names):
            field = np.array(f["d_" + field_i + f"_{slice}"])

            ax[i].tick_params(axis="both", which="both", direction="in", color="white", labeltop=False, 
                              labelbottom=False, labelleft=False, labelright=False, top=1, right=1, bottom=1,
                              left=1)
            
            im = ax[i].imshow(field[y_start:y_end, x_start:x_end] / gas_density[y_start:y_end, x_start:x_end], origin="lower", vmin=vmin, vmax=vmax, extent=[0, xlen, 0, ylen], cmap=cmap)
            ax[i].text(.96, .85, f"{labels[i]}", horizontalalignment='right', verticalalignment='center', transform = ax[i].transAxes, color="white")
            
            ax[i].set_xticks(xticks)
            ax[i].set_yticks(yticks)
            print(xticks)
            print(yticks)
            
            if i == 2:
                ax[i].hlines(spacing/2.5, 4*spacing, 5*spacing, linewidth=linewidth, colors="white")
                ax[i].text(5*spacing+0.07, spacing/2.5, sbar_label, ha="left", va="center", color="white")
            
            # divider = make_axes_locatable(ax[i])
            # cax = divider.append_axes("right", size="5%", pad=0.05)
            fig.subplots_adjust(right=0.9)
            # cbar_ax = fig.add_axes([0.952, 0.016, 0.05, 0.968])
            cbar_ax = fig.add_axes([0.952, 0.0297, 0.05, panel_height/total_height+0.031])
            cbar = fig.colorbar(im, cax=cbar_ax)
            cbar.set_label(clabel, rotation=270, labelpad=15)
            cbar.ax.tick_params(axis="y", direction="in", color="white")

            if (i == 0):
                ax[i].text(.96, .15, f"{t/1e3:.0f} Myr", horizontalalignment='right', verticalalignment='center', transform = ax[i].transAxes, color="white")

        plt.tight_layout()
        fig.savefig(pngdir + f"/{fnum}_dtg_zoom_{mode}.png", dpi=300, bbox_inches="tight")
        plt.close()

        print(f"Saving figure {fnum} of {ne}.\n")

if __name__ == "__main__":
    args = read_cmdline()

    basedir = args.basedir
    field_names = args.field_names
    ns = args.nstart
    ne = args.nend
    vmin = args.cbar_lower
    vmax = args.cbar_upper
    slice = args.slice
    mode = args.mode

    sys.path.insert(0, args.configdir)
    import hconfig

    main(basedir, field_names, ns, ne, vmin, vmax, slice, mode)
