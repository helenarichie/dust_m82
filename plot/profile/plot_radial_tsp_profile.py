import matplotlib.pyplot as plt
import numpy as np
import os
import pathlib
import sys
import seaborn as sns
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent.resolve(), "../../utils/"))
from read_cmdline import read_cmdline
from read_radial_profile import read_radial_profile
from calc_cooling_time import calc_cooling_time
from calc_tau_sp import calc_tau_sp

def main(basedir, outdir, fig_name, time, simulation, weight, tail):
    fnum = int(time * 2 / 100)

    radial_dir = os.path.join(basedir, "profiles/radial/")

    bin_tot, _, _, density_hot, _, temp_hot, _, _, _, _ = read_radial_profile(radial_dir, fnum, simulation, "hot", weight, tail)
    _, _, _, density_cool, _, temp_cool, _, _, _, _ = read_radial_profile(radial_dir, fnum, simulation, "cold", weight, tail)

    bin_tot = np.array(bin_tot)

    # median values
    density_hot, density_cool, temp_hot, temp_cool = np.array(density_hot[1]), np.array(density_cool[1]), np.array(temp_hot[1]), np.array(temp_cool[1])

    density_mixed = np.sqrt(density_cool * density_hot)
    temp_mixed = np.sqrt(temp_cool * temp_hot)

    t_cool_mixed = []
    for coord in zip(density_mixed, temp_mixed):
        t_cool_mixed.append(calc_cooling_time(coord[0], coord[1]))
    t_cool_mixed = np.array(t_cool_mixed)

    color_hot, color_mixed, color_cool = sns.color_palette(palette="flare", n_colors=3)
    linewidth = 3
    fontsize = 20
    plt.rcParams["font.size"] = fontsize

    plt.figure(figsize=(8, 6))

    plt.tick_params(axis="both", which="both", top=True, right=True)

    plt.plot(bin_tot, calc_tau_sp(density_mixed, temp_mixed, .1)*1e-6, label=r"mixed, m82", color=color_mixed, linestyle="solid", linewidth=linewidth)
    plt.plot(bin_tot, calc_tau_sp(density_hot, temp_hot, .1)*1e-6, label=r"hot, m82", color=color_hot, linestyle="solid", linewidth=linewidth)

    wh_rad = np.argmin(abs(bin_tot-1))
    print(f"m82 cooling time at 1 kpc: {t_cool_mixed[wh_rad]/1e6:1e} Myr, {density_mixed[wh_rad]:1e} cm^-3, {temp_mixed[wh_rad]:1e} K, {temp_hot[wh_rad]:1e} K")

    ################# highz #################
    radial_dir = os.path.join("/Users/helenarichie/Desktop/2024-10-25/profiles/radial/")
    _, _, _, density_hot, _, temp_hot, _, _, _, _ = read_radial_profile(radial_dir, fnum, "highz", "hot", weight, tail)
    _, _, _, density_cool, _, temp_cool, _, _, _, _ = read_radial_profile(radial_dir, fnum, "highz", "cold", weight, tail)
     # median values
    density_hot, density_cool, temp_hot, temp_cool = np.array(density_hot[1]), np.array(density_cool[1]), np.array(temp_hot[1]), np.array(temp_cool[1])
    density_mixed = np.sqrt(density_cool * density_hot)
    temp_mixed = np.sqrt(temp_cool * temp_hot)
    t_cool_mixed = []
    for coord in zip(density_mixed, temp_mixed):
        t_cool_mixed.append(calc_cooling_time(coord[0], coord[1]))
    t_cool_mixed = np.array(t_cool_mixed)

    plt.plot(bin_tot, calc_tau_sp(density_mixed, temp_mixed, .1)*1e-6, label=r"mixed, high-z", color=color_mixed, linestyle="dashed", linewidth=linewidth)
    plt.plot(bin_tot, calc_tau_sp(density_hot, temp_hot, .1)*1e-6, label=r"hot, high-z", color=color_hot, linestyle="dashed", linewidth=linewidth)

    print(f"highz cooling time at 1 kpc: {t_cool_mixed[wh_rad]/1e6:1e} Myr, {density_mixed[wh_rad]:1e} cm^-3, {temp_mixed[wh_rad]:1e} K, {temp_hot[wh_rad]:1e} K")

    plt.xlabel("r [kpc]")
    plt.ylabel(r"$t_{sp}(a=0.01~\mu m)$ [Myr]")
    plt.legend(loc="lower right", fontsize=fontsize-3)

    plt.xlim(0, 5)
    plt.ylim(0, 30)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, fig_name), dpi=300)
    plt.close()

if __name__ == "__main__":
    args = read_cmdline()

    sys.path.insert(0, args.configdir)
    import hconfig

    basedir = args.basedir
    time = args.time
    weight = args.weight
    tail = args.tail
    simulation = args.simulation
    outdir = args.outdir
    fig_name = args.fig_name


    main(basedir, outdir, fig_name, time, simulation, weight, tail)