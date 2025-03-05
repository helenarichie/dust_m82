import argparse
import h5py
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import os
import seaborn as sns
import sys
sys.path.append("../calc/")
from calc_temp import calc_temp_DE

def read_cmdline():
    p = argparse.ArgumentParser()
    p.add_argument("-b", "--basedir", type=str, required=True)
    p.add_argument("-c", "--configdir", type=str, required=True)
    p.add_argument("-s", "--nstart", type=int, required=True)
    p.add_argument("-e", "--nend", type=int, required=True)
    p.add_argument("-p", "--plot-lines", required=False, action="store_false")
    p.add_argument("-d", "--slice", type=str, choices=["xz", "xy"], required=False, default="xz")
    p.add_argument("-m", "--mode", type=str, choices=["dark", "light"], required=False, default="light")
    p.add_argument("--angle", type=float)
    
    args = p.parse_args()
    return args
    
def main(basedir, ns, ne, slice, mode, plot_lines, angle):
    # define data directories
    datadir = os.path.join(basedir, "hdf5", "slice")
    pngdir = os.path.join(basedir, "png", "gas_slice")

    # set plotting style
    if mode == "dark":
        plt.style.use('dark_background')

    cmap_gas = sns.color_palette("mako", as_cmap=True)
    cmap_temp = sns.color_palette("flare_r", as_cmap=True)
    matplotlib.rcParams.update({'font.size': 15})
    clabel_dens = r'$\log_{10}(\rho_{gas}~[M_\odot\,kpc^{-3}])$'
    clabel_temp = r'$\log_{10}(T~[K])$'

    if slice == "xz":
        xticks = [2, 4, 6, 8]
        yticks = [2, 4, 6, 8, 10, 12, 14, 16, 18]
    if slice == "xy":
        xticks = yticks = [2, 4, 6, 8]
    sbar_x, sbar_y = 2, 1
    text_x = sbar_x - 0.2
    sbar_label = "2 kpc"
    linewidth = 2
    panel_width = 5
    cbar_width = 0.3
    fig_width = 2 * panel_width + 2 * cbar_width
    cbar_gridspec = (panel_width + cbar_width) / panel_width
    if slice == "xz":
        time_x, time_y = 9.5, 19
    if slice == "xy":
        time_x, time_y = 8.25, 9.25

    width_ratios = [cbar_gridspec, cbar_gridspec]
    width_pad = 0.2

    vlim_dens = [2.9, 10]
    vlim_temp = [4, 8.2]

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
        density_unit = head["density_unit"]
        velocity_unit = head["velocity_unit"]
        energy_unit = head["energy_unit"]
        
        gas_density = np.array(f["d_" + f"{slice}"])
        momentum_x = np.array(f["mx_" + f"{slice}"])
        momentum_y = np.array(f["mx_" + f"{slice}"])
        momentum_z = np.array(f["mx_" + f"{slice}"])
        energy = np.array(f["E_" + f"{slice}"])
        gas_energy = np.array(f["GE_" + f"{slice}"])

        temperature = calc_temp_DE(gamma, mu, MP, KB, gas_density, gas_energy, density_unit, velocity_unit)

        if slice == "xz":
            xlen = nx*dx
            ylen = nz*dx
            aspect = nz / nx
        if slice == "xy":
            xlen = nx*dx
            ylen = ny*dx
            aspect = ny / nx

        fig, ax = plt.subplots(1, 2, figsize=(fig_width + 2 * width_pad, aspect * panel_width), gridspec_kw={"width_ratios":width_ratios, "wspace":width_pad, "hspace":0})
        
        for ax_i in ax:
            ax_i.tick_params(axis="both", which="both", direction="in", color="white", labeltop=False, 
                            labelbottom=False, labelleft=False, labelright=False, top=1, right=1, bottom=1,
                            left=1)
            ax_i.set_xticks(xticks)
            ax_i.set_yticks(yticks)

        im_dens = ax[0].imshow(np.log10(gas_density.T), origin="lower", vmin=vlim_dens[0], vmax=vlim_dens[1], extent=[0, xlen, 0, ylen], cmap=cmap_gas, aspect="auto", zorder=-1)
        im_temp = ax[1].imshow(np.log10(temperature.T), origin="lower", vmin=vlim_temp[0], vmax=vlim_temp[1], extent=[0, xlen, 0, ylen], cmap=cmap_temp, aspect="auto", zorder=-1)

        if plot_lines:
            y_lines = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
            for y in y_lines:
                ax[0].hlines(y, 0, 10, linewidth=linewidth-1, colors="white", alpha=0.7, zorder=0, linestyle="--")

            phi_right = np.radians(90 - angle)
            phi_left = np.radians(90 + angle)
            ax[0].axline((5, 10), slope=np.tan(phi_right), color="white", alpha=0.7, linewidth=linewidth-1, zorder=0)
            ax[0].axline((5, 10), slope=np.tan(phi_left), color="white", alpha=0.7, linewidth=linewidth-1, zorder=0)
            
            ax[1].hlines(sbar_y, sbar_x, sbar_x + (xticks[1] - xticks[0]), linewidth=linewidth, colors="white")
            ax[1].text(text_x, sbar_y, sbar_label, ha="right", va="center", color="white")
        else:
            # phi_right = np.radians(90 - angle)
            # phi_left = np.radians(90 + angle)
            # ax[0].axline((5, 10), slope=np.tan(phi_right), color="white", alpha=0.7, linewidth=linewidth-1, zorder=0)
            # ax[0].axline((5, 10), slope=np.tan(phi_left), color="white", alpha=0.7, linewidth=linewidth-1, zorder=0)
            
            ax[0].hlines(sbar_y, sbar_x, sbar_x + (xticks[1] - xticks[0]), linewidth=linewidth, colors="white")
            ax[0].text(text_x, sbar_y, sbar_label, ha="right", va="center", color="white")

        divider = make_axes_locatable(ax[0])
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar = fig.colorbar(im_dens, ax=ax[0], cax=cax)
        cbar.set_label(clabel_dens, rotation=270, labelpad=25, fontsize=18)
        cbar.ax.tick_params(axis="y", direction="in", color="white")
        
        divider = make_axes_locatable(ax[1])
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar = fig.colorbar(im_temp, ax=ax[1], cax=cax)
        cbar.set_label(clabel_temp, rotation=270, labelpad=25, fontsize=18)
        cbar.ax.tick_params(axis="y", direction="in", color="white")

        ax[1].text(time_x, time_y, f"{t/1e3:.0f} Myr", ha="right", va="center", color="white")

        fig.savefig(pngdir + f"/{fnum}_gas_slice_{slice}_{mode}.png", dpi=300, bbox_inches="tight")
        plt.close()

        print(f"Saving figure {fnum} of {ne}.\n")

if __name__ == "__main__":
    args = read_cmdline()

    basedir = args.basedir
    ns = args.nstart
    ne = args.nend
    slice = args.slice
    mode = args.mode
    plot_lines = args.plot_lines
    angle = args.angle

    sys.path.insert(0, args.configdir)
    import hconfig

    main(basedir, ns, ne, slice, mode, plot_lines, angle)
