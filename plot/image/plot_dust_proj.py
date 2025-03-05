import argparse
import h5py
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import os
import pathlib
import seaborn as sns
import sys
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent.resolve(), "../../utils/"))
from read_cmdline import read_cmdline

def main(basedir, field_names, ns, ne, mode, vmin=0, vmax=8):
    # define data directories
    datadir = os.path.join(basedir, "hdf5", "proj")
    pngdir = os.path.join(basedir, "png", "dust_proj")

    # set plotting style
    if mode == "dark":
        plt.style.use('dark_background')

    matplotlib.rcParams.update({'font.size': 15})

    cmap = sns.color_palette("rocket", as_cmap=True)
    clabel = r'$\mathrm{log}_{10}(\Sigma_{dust})$ [$\mathrm{M}_\odot\,\mathrm{kpc}^{-2}$]'

    xticks = [2, 4, 6, 8]
    yticks = [2, 4, 6, 8, 10, 12, 14, 16, 18]
    sbar_x, sbar_y = 2, 1
    text_x = sbar_x - 0.2
    sbar_label = "2 kpc"
    linewidth = 2
    panel_width = 5
    cbar_width = 0.3
    fig_width = len(field_names) * panel_width + cbar_width
    cbar_gridspec = (panel_width + cbar_width) / panel_width
    time_x, time_y = 9.5, 19

    width_ratios = []
    for i in field_names:
        width_ratios.append(1)
    width_ratios[-1] = cbar_gridspec

    # define physical constants
    mu = 0.6 # mean molecular weight
    MP = 1.672622e-24 # proton mass, g
    KB = 1.380658e-16 # Boltzmann constant, cm^2 g s^-2 K^-1

    for fnum in range(ns, ne+1):
        f = h5py.File(os.path.join(datadir, str(fnum)+"_proj.h5"), "r")

        head = f.attrs
        dx = head["dx"][0]
        t = head["t"][0]
        gamma = head["gamma"][0]
        nx, ny, nz = head["dims"][0], head["dims"][1], head["dims"][2]
        dx = head["dx"][0]
        xlen = nx*dx
        ylen = nz*dx

        aspect = nz / nx

        fig, ax = plt.subplots(1, len(field_names), figsize=(fig_width, aspect * panel_width), gridspec_kw={"width_ratios":width_ratios, "wspace":0, "hspace":0})

        if len(field_names) == 1:
            ax = [ax]
        
        if len(field_names) != 1:
            for ax_i in ax:
                for child in ax_i.get_children():
                    if isinstance(child, matplotlib.spines.Spine):
                        child.set_color("white")

        for i, field_i in enumerate(field_names):
            field = np.array(f["d_" + field_i + f"_xz"])

            field[field==0] = sys.float_info.min

            ax[i].tick_params(axis="both", which="both", direction="in", color="white", labeltop=False, 
                              labelbottom=False, labelleft=False, labelright=False, top=1, right=1, bottom=1,
                              left=1)
            im = ax[i].imshow(np.log10(field.T), origin="lower", vmin=vmin, vmax=vmax, extent=[0, xlen, 0, ylen], cmap=cmap,
                              aspect="auto")
            
            ax[i].set_xticks(xticks)
            ax[i].set_yticks(yticks)
            
            if i == 0:
                ax[i].hlines(sbar_y, sbar_x, sbar_x + (xticks[1] - xticks[0]), linewidth=linewidth, colors="white")
                ax[i].text(text_x, sbar_y, sbar_label, ha="right", va="center", color="white")
            
            if (i == len(field_names)-1):
                divider = make_axes_locatable(ax[i])
                cax = divider.append_axes("right", size="5%", pad=0.05)
                cbar = fig.colorbar(im, ax=ax[i], cax=cax)
                cbar.set_label(clabel, rotation=270, labelpad=25, fontsize=18)
                cbar.ax.tick_params(axis="y", direction="in", color="white")
                ax[i].text(time_x, time_y, f"{t/1e3:.0f} Myr", ha="right", va="center", color="white")

            if field_i == "dust_0":
                size_label = r"$1~{\mu m}$"
            if field_i == "dust_1":
                size_label = r"$0.1~{\mu m}$"
            if field_i == "dust_2":
                size_label = r"$0.01~{\mu m}$"
            if field_i == "dust_3":
                size_label = r"$0.001~{\mu m}$"

            ax[i].text(0.5, time_y, size_label, ha="left", va="center", color="white")

        fig.savefig(pngdir + f"/{fnum}_dust_proj_{mode}_{len(field_names)}.png", dpi=300, bbox_inches="tight")
        plt.close()
       
        print(f"Saving figure {fnum} of {ne}.\n") 
        
if __name__ == "__main__":
    args = read_cmdline()

    basedir = args.basedir
    field_names = args.field_names
    ns = args.nstart
    ne = args.nend
    vmin = args.ymin
    vmax = args.ymax
    mode = args.mode

    sys.path.insert(0, args.configdir)
    import hconfig

    mode = "light"
    if args.mode == "dark":
        mode = "dark"

    main(basedir, field_names, ns, ne, mode, vmin, vmax)
