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
    p.add_argument("-s", "--nstart", type=int, required=True)
    p.add_argument("-e", "--nend", type=int, required=True)
    p.add_argument("-m", "--mode", type=str, choices=["dark", "light"], required=False, default="light")
    args = p.parse_args()
    return args

def main(basedir, ns, ne, mode):
    # define data directories
    datadir = os.path.join(basedir, "hdf5", "proj")
    pngdir = os.path.join(basedir, "png", "dust_proj")

    # set plotting style
    if mode == "dark":
        plt.style.use('dark_background')
    matplotlib.rcParams.update({'font.size': 15})
    cmap = sns.color_palette("rocket", as_cmap=True)
    clabel = r'$\mathrm{log}_{10}(\Sigma_{dust})$ [$\mathrm{M}_\odot\,\mathrm{kpc}^{-2}$]'
    # fields to read from HDF5 file
    fields = ["d_dust_0_xz", "d_dust_1_xz", "d_dust_2_xz", "d_dust_3_xz"]
    xticks = [2, 4, 6, 8]
    yticks = [2, 4, 6, 8, 10, 12, 14, 16, 18]
    sbar_x, sbar_y = 2, 1
    sbar_label = "2 kpc"
    linewidth = 2
    panel_width = 5
    cbar_width = 0.3
    fig_width = len(fields) * panel_width + cbar_width
    cbar_gridspec = (panel_width + cbar_width) / panel_width
    time_x, time_y = 8, 19

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

        fig, ax = plt.subplots(1, 4, figsize=(fig_width, 2 * panel_width), gridspec_kw={"width_ratios":[1, 1, 1, cbar_gridspec], "wspace":0, "hspace":0})
        
        for ax_i in ax:
            for child in ax_i.get_children():
                if isinstance(child, matplotlib.spines.Spine):
                    child.set_color("white")

        for i, field_i in enumerate(fields):
            field = np.array(f[field_i])

            ax[i].tick_params(axis="both", which="both", direction="in", color="white", labeltop=False, 
                              labelbottom=False, labelleft=False, labelright=False, top=1, right=1, bottom=1,
                              left=1)
            im = ax[i].imshow(np.log10(field.T), origin="lower", vmin=1, vmax=8, extent=[0, xlen, 0, ylen], cmap=cmap,
                              aspect="auto")
            
            ax[i].set_xticks(xticks)
            ax[i].set_yticks(yticks)
            
            if i == 0:
                ax[i].hlines(sbar_y, sbar_x, sbar_x + (xticks[1] - xticks[0]), linewidth=linewidth, colors="white")
                ax[i].text(sbar_x - 0.2, sbar_y, sbar_label, ha="right", va="center", color="white")
            
            if i == 3:
                divider = make_axes_locatable(ax[i])
                cax = divider.append_axes("right", size="5%", pad=0.05)
                cbar = fig.colorbar(im, ax=ax[i], cax=cax)
                cbar.set_label(clabel)
                cbar.ax.tick_params(axis="y", direction="in", color="white")
                ax[i].text(time_x, time_y, f"{t/1e3:.0f} Myr", ha="left", va="center", color="white")

        fig.savefig(pngdir + f"/{fnum}_dust_proj.png", dpi=300, bbox_inches="tight")
        plt.close()
       
        print(f"Saving figure {fnum} of {ne}.\n") 
        
if __name__ == "__main__":
    args = read_cmdline()

    basedir = args.basedir
    ns = args.nstart
    ne = args.nend

    sys.path.insert(0, args.configdir)
    import hconfig

    mode = "light"
    if args.mode == "dark":
        mode = "dark"

    main(basedir, ns, ne, mode)
