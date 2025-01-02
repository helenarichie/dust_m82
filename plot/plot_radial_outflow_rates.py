import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import sys

def read_cmdline():
    p = argparse.ArgumentParser()
    p.add_argument("-b", "--basedir", type=str, required=True)
    p.add_argument("-c", "--configdir", type=str, required=True)
    p.add_argument("-f", "--fnum", type=int, required=True)
    p.add_argument("-s", "--simulation", type=str, required=True)
    p.add_argument("-t", "--tail", type=str, required=False, default="")
    p.add_argument("-r", "--rmask", type=int, required=False, default=0)
    p.add_argument("-m", "--mode", type=str, choices=["dark", "light"], required=False, default="light")
    args = p.parse_args()
    return args

def main(basedir, fnum, simulation, tail, r_mask, mode):
    N_bins = 80
    r_mask = 0
    time = fnum * 50 / 1e3

    f_name = f"{fnum}_prof_{simulation}_outflow{tail}.txt"

    bins = []
    gas_rate_hot = []
    momentum_rate_hot = []
    energy_rate_hot = []
    gas_rate_mixed = []
    momentum_rate_mixed = []
    energy_rate_mixed = []
    gas_rate_cool = []
    momentum_rate_cool = []
    energy_rate_cool = []
    dust_0_rate_hot = []
    dust_0_rate_mixed = []
    dust_0_rate_cool = []
    dust_1_rate_hot = []
    dust_1_rate_mixed = []
    dust_1_rate_cool = []
    dust_2_rate_hot = []
    dust_2_rate_mixed = []
    dust_2_rate_cool = []
    dust_3_rate_hot = []
    dust_3_rate_mixed = []
    dust_3_rate_cool = []

    parse = False

    with open(os.path.join(basedir, f_name)) as f:
        line_i = 0
        for line in f:
            if parse:
                line_i += 1
                line = line.strip(" ").rstrip("\n").split(",")
                bins.append(float(line[0]))
                # hot
                gas_rate_hot.append(float(line[2]))
                momentum_rate_hot.append(float(line[3]))
                energy_rate_hot.append(float(line[4]))
                # mixed
                gas_rate_mixed.append(float(line[6]))
                momentum_rate_mixed.append(float(line[7]))
                energy_rate_mixed.append(float(line[8]))
                # cool
                gas_rate_cool.append(float(line[10]))
                momentum_rate_cool.append(float(line[11]))
                energy_rate_cool.append(float(line[12]))
                # dust_0
                dust_0_rate_hot.append(float(line[13]))
                dust_0_rate_mixed.append(float(line[14]))
                dust_0_rate_cool.append(float(line[15]))
                # dust_1
                dust_1_rate_hot.append(float(line[16]))
                dust_1_rate_mixed.append(float(line[17]))
                dust_1_rate_cool.append(float(line[18]))
                # dust_2
                dust_2_rate_hot.append(float(line[19]))
                dust_2_rate_mixed.append(float(line[20]))
                dust_2_rate_cool.append(float(line[21]))
                # dust_3
                dust_3_rate_hot.append(float(line[22]))
                dust_3_rate_mixed.append(float(line[23]))
                dust_3_rate_cool.append(float(line[24]))
            elif line.startswith("# Radial bin"):
                parse = True

    bins = np.array(bins)
    gas_rate_hot = np.array(gas_rate_hot)
    gas_rate_mixed = np.array(gas_rate_mixed)
    gas_rate_cool = np.array(gas_rate_cool)
    energy_rate_hot = np.array(energy_rate_hot)
    energy_rate_mixed = np.array(energy_rate_mixed)
    energy_rate_cool = np.array(energy_rate_cool)
    momentum_rate_hot = np.array(momentum_rate_hot)
    momentum_rate_mixed = np.array(momentum_rate_mixed)
    momentum_rate_cool = np.array(momentum_rate_cool)
    dust_0_rate_hot = np.array(dust_0_rate_hot)
    dust_0_rate_mixed = np.array(dust_0_rate_mixed)
    dust_0_rate_cool = np.array(dust_0_rate_cool)
    dust_1_rate_hot = np.array(dust_1_rate_hot)
    dust_1_rate_mixed = np.array(dust_1_rate_mixed)
    dust_1_rate_cool = np.array(dust_1_rate_cool)
    dust_2_rate_hot = np.array(dust_2_rate_hot)
    dust_2_rate_mixed = np.array(dust_2_rate_mixed)
    dust_2_rate_cool = np.array(dust_2_rate_cool)
    dust_3_rate_hot = np.array(dust_3_rate_hot)
    dust_3_rate_mixed = np.array(dust_3_rate_mixed)
    dust_3_rate_cool = np.array(dust_3_rate_cool)

    gas_color = "mediumturquoise"
    energy_color = "mediumorchid"
    momentum_color = "palevioletred"
    linewidth = 3
    hot_style = "solid"
    mixed_style = "dashed"
    cool_style = "dashdot"

    cool_color = "cornflowerblue"
    mixed_color = "mediumseagreen"
    hot_color = "red"
    tot_color = "black"

    if mode == "dark":
        plt.style.use('dark_background')

    plt.plot(bins[bins>r_mask], gas_rate_hot[bins>r_mask] * 1e-3, c=hot_color, linewidth=linewidth, label="hot")
    plt.plot(bins[bins>r_mask], gas_rate_mixed[bins>r_mask] * 1e-3, c=mixed_color, linewidth=linewidth, label="mixed")
    plt.plot(bins[bins>r_mask], gas_rate_cool[bins>r_mask] * 1e-3, c=cool_color, linewidth=linewidth, label="cool")
    plt.plot(bins[bins>r_mask], (gas_rate_cool[bins>r_mask]+gas_rate_mixed[bins>r_mask]+gas_rate_hot[bins>r_mask]) * 1e-3, c=tot_color, linewidth=linewidth, label="tot")
    plt.title(rf"$t={round(time, 1)}$ Myr")
    plt.xlabel("r [kpc]")
    plt.ylabel(r"$\dot{M}$ $[M_\odot\,yr^{-1}]$")
    plt.legend()
    plt.savefig(os.path.join(basedir, "png", f"{fnum}_gas_outflow{tail}.png"), dpi=300)
    plt.close()

    plt.plot(bins[bins>r_mask], momentum_rate_hot[bins>r_mask], c=hot_color, linewidth=linewidth, label="hot")
    plt.plot(bins[bins>r_mask], momentum_rate_mixed[bins>r_mask], c=mixed_color, linewidth=linewidth, label="mixed")
    plt.plot(bins[bins>r_mask], momentum_rate_cool[bins>r_mask], c=cool_color, linewidth=linewidth, label="cool")
    plt.plot(bins[bins>r_mask], momentum_rate_cool[bins>r_mask]+momentum_rate_mixed[bins>r_mask]+momentum_rate_hot[bins>r_mask], c=tot_color, linewidth=linewidth, label="tot")
    plt.title(rf"$t={round(time, 1)}$ Myr")
    plt.xlabel("r [kpc]")
    plt.ylabel(r"$\dot{p}$ $[M_\odot\,km\,s^{-1}\,yr^{-1}]$")
    plt.legend()
    plt.savefig(os.path.join(basedir, "png", f"{fnum}_momentum_outflow{tail}.png"), dpi=300)
    plt.close()

    plt.semilogy(bins[bins>r_mask], energy_rate_hot[bins>r_mask], c=hot_color, linewidth=linewidth, label="hot")
    plt.semilogy(bins[bins>r_mask], energy_rate_mixed[bins>r_mask], c=mixed_color, linewidth=linewidth, label="mixed")
    plt.semilogy(bins[bins>r_mask], energy_rate_cool[bins>r_mask], c=cool_color, linewidth=linewidth, label="cool")
    plt.semilogy(bins[bins>r_mask], energy_rate_cool[bins>r_mask]+energy_rate_mixed[bins>r_mask]+energy_rate_hot[bins>r_mask], c=tot_color, linewidth=linewidth, label="tot")
    plt.title(rf"$t={round(time, 1)}$ Myr")
    plt.xlabel("r [kpc]")
    plt.ylabel(r"$\dot{E}$ $[erg\,s^{-1}]$")
    plt.legend()
    plt.savefig(os.path.join(basedir, "png", f"{fnum}_energy_outflow{tail}.png"), dpi=300)
    plt.close()

    color_hot, color_mixed, color_cool = sns.color_palette(palette="flare", n_colors=3)
    # styles = ["solid", "dotted", "dashed", "dashdot"]
    styles = ["dashdot", "dotted", "dashed", "solid"]
    # plt.plot(0, 0, linestyle=styles[0], label=r"$a=1~\mu$m", c="k", linewidth=linewidth)
    plt.plot(0, 0, linestyle=styles[1], label=r"$a=0.1~\mu$m", c="k", linewidth=linewidth)
    plt.plot(0, 0, linestyle=styles[2], label=r"$a=0.01~\mu$m", c="k", linewidth=linewidth)
    plt.plot(0, 0, linestyle=styles[3], label=r"$a=0.001~\mu$m", c="k", linewidth=linewidth)
    # plt.plot(0, 0, label=r"hot", c=color_hot, linewidth=linewidth)
    # plt.plot(0, 0, label=r"mixed", c=color_mixed, linewidth=linewidth)
    # plt.plot(0, 0, label=r"cool", c=color_cool, linewidth=linewidth)

    # plt.plot(bins[bins>r_mask], dust_0_rate_hot[bins>r_mask], c=color_hot, linewidth=linewidth, linestyle=styles[0])
    # plt.plot(bins[bins>r_mask], dust_0_rate_mixed[bins>r_mask], c=color_mixed, linewidth=linewidth, linestyle=styles[0])
    # plt.plot(bins[bins>r_mask], dust_0_rate_cool[bins>r_mask], c=color_cool, linewidth=linewidth, linestyle=styles[0])
    # plt.plot(bins[bins>r_mask], dust_0_rate_cool[bins>r_mask]+dust_0_rate_mixed[bins>r_mask]+dust_0_rate_hot[bins>r_mask], c=tot_color, linewidth=linewidth, label="total dust_0", linestyle=styles[0])

    plt.plot(bins[bins>r_mask], dust_1_rate_hot[bins>r_mask], c=color_hot, linewidth=linewidth, linestyle=styles[1])
    plt.plot(bins[bins>r_mask], dust_2_rate_hot[bins>r_mask], c=color_hot, linewidth=linewidth, linestyle=styles[2])
    plt.plot(bins[bins>r_mask], dust_3_rate_hot[bins>r_mask], c=color_hot, linewidth=linewidth, linestyle=styles[3])
    plt.xlim(np.amin(bins[bins>r_mask]), np.amax(bins[bins>r_mask]))
    # plt.title(rf"$t={round(time, 1)}$ Myr")
    plt.xlabel("r [kpc]", fontsize=15)
    plt.ylabel(r"$\dot{M}$ $[M_\odot\,yr^{-1}]$", fontsize=15)
    plt.xlim(np.amin(bins[bins>r_mask]), np.amax(bins[bins>r_mask]))
    # plt.ylim(0-0.3, 7)
    # plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(basedir, "png", f"{fnum}_hot_outflow{tail}.png"), dpi=300)
    plt.close()

    plt.plot(bins[bins>r_mask], dust_1_rate_mixed[bins>r_mask], c=color_mixed, linewidth=linewidth, linestyle=styles[1])
    plt.plot(bins[bins>r_mask], dust_2_rate_mixed[bins>r_mask], c=color_mixed, linewidth=linewidth, linestyle=styles[2])
    plt.plot(bins[bins>r_mask], dust_3_rate_mixed[bins>r_mask], c=color_mixed, linewidth=linewidth, linestyle=styles[3])
    plt.xlim(np.amin(bins[bins>r_mask]), np.amax(bins[bins>r_mask]))
    # plt.title(rf"$t={round(time, 1)}$ Myr")
    plt.xlabel("r [kpc]", fontsize=15)
    plt.ylabel(r"$\dot{M}$ $[M_\odot\,yr^{-1}]$", fontsize=15)
    plt.xlim(np.amin(bins[bins>r_mask]), np.amax(bins[bins>r_mask]))
    # plt.ylim(0-0.3, 7)
    # plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(basedir, "png", f"{fnum}_mixed_outflow{tail}.png"), dpi=300)
    plt.close()

    plt.plot(bins[bins>r_mask], dust_1_rate_cool[bins>r_mask], c=color_cool, linewidth=linewidth, linestyle=styles[1])
    plt.plot(bins[bins>r_mask], dust_2_rate_cool[bins>r_mask], c=color_cool, linewidth=linewidth, linestyle=styles[2])
    plt.plot(bins[bins>r_mask], dust_3_rate_cool[bins>r_mask], c=color_cool, linewidth=linewidth, linestyle=styles[3])
    plt.plot(0, 0, linestyle=styles[1], label=r"$a=0.1~\mu$m", c="k", linewidth=linewidth)
    plt.plot(0, 0, linestyle=styles[2], label=r"$a=0.01~\mu$m", c="k", linewidth=linewidth)
    plt.plot(0, 0, linestyle=styles[3], label=r"$a=0.001~\mu$m", c="k", linewidth=linewidth)
    plt.xlim(np.amin(bins[bins>r_mask]), np.amax(bins[bins>r_mask]))
    # plt.ylim(0-0.3, 7)
    # plt.title(rf"$t={round(time, 1)}$ Myr")
    plt.xlabel("r [kpc]", fontsize=13)
    plt.ylabel(r"$\dot{M}$ $[M_\odot\,yr^{-1}]$", fontsize=15)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(basedir, "png", f"{fnum}_cool_outflow{tail}.png"), dpi=300)
    plt.close()

if __name__ == "__main__":
    args = read_cmdline()

    sys.path.insert(0, args.configdir)
    import hconfig

    basedir = args.basedir
    fnum = args.fnum
    simulation = args.simulation
    tail = args.tail
    r_mask = args.rmask
    mode = args.mode

    main(basedir, fnum, simulation, tail, r_mask, mode)