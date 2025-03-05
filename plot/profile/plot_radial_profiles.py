import argparse
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import sys
import pathlib
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent.resolve(), "../utils/"))
from read_cmdline import read_cmdline


def main(basedir, outdir, fnum, simulation, phase, weight, tail, r_mask, mode, field_names):
    N_bins = 80
    time = fnum * 50 / 1e3

    f_name = f"{fnum}_prof_{simulation}_{phase}_{weight}{tail}.txt"

    parse_totals = False
    parse_stats = False

    bin_tot = []
    m_gas = []
    m_dust_0 = []
    m_dust_1 = []
    m_dust_2 = []
    m_dust_3 = []

    cell_count = []
    gas_avg = []
    gas_med = []
    gas_lo = []
    gas_hi = []
    temp_avg = []
    temp_med = []
    temp_lo = []
    temp_hi = []
    v_avg = []
    v_med = []
    v_lo = []
    v_hi = []
    P_avg = []
    P_med = []
    P_lo = []
    P_hi = []
    S_avg = []
    S_med = []
    S_lo = []
    S_hi = []
    M_avg = []
    M_med = []
    M_lo = []
    M_hi = []

    with open(os.path.join(basedir, f_name)) as f:
        line_i = 0
        for line in f:
            if parse_totals:
                line_i += 1
                line = line.strip(" ").rstrip("\n").split(",")
                bin_tot.append(float(line[0]))
                m_gas.append(float(line[1]))
                m_dust_0.append(float(line[2]))
                m_dust_1.append(float(line[3]))
                m_dust_2.append(float(line[4]))
                m_dust_3.append(float(line[5]))
                if line_i == N_bins:
                    parse_totals = False
                    line_i = 0
            
            elif parse_stats:
                line_i += 1
                line = line.rstrip("\n").split(",")
                for i, entry in enumerate(line):
                    if i == 1:
                        entry = entry.strip(" ")
                        cell_count.append(int(entry[0]))
                    if i == 2:
                        entry = entry.split(" ")
                        while("" in entry):
                            entry.remove("")
                        gas_avg.append(float(entry[1]))
                        gas_med.append(float(entry[2]))
                        gas_lo.append(float(entry[3]))
                        gas_hi.append(float(entry[4]))
                    if i == 3:
                        entry = entry.split(" ")
                        while("" in entry):
                            entry.remove("")
                        v_avg.append(float(entry[0]))
                        v_med.append(float(entry[1]))
                        v_lo.append(float(entry[2]))
                        v_hi.append(float(entry[3]))
                    if i == 4:
                        entry = entry.split(" ")
                        while("" in entry):
                            entry.remove("")
                        temp_avg.append(float(entry[0]))
                        temp_med.append(float(entry[1]))
                        temp_lo.append(float(entry[2]))
                        temp_hi.append(float(entry[3]))
                    if i == 5:
                        entry = entry.split(" ")
                        while("" in entry):
                            entry.remove("")
                        P_avg.append(float(entry[0]))
                        P_med.append(float(entry[1]))
                        P_lo.append(float(entry[2]))
                        P_hi.append(float(entry[3]))
                    if i == 6:
                        entry = entry.split(" ")
                        while("" in entry):
                            entry.remove("")
                        S_avg.append(float(entry[0]))
                        S_med.append(float(entry[1]))
                        S_lo.append(float(entry[2]))
                        S_hi.append(float(entry[3]))
                    if i == 7:
                        entry = entry.split(" ")
                        while("" in entry):
                            entry.remove("")
                        M_avg.append(float(entry[0]))
                        M_med.append(float(entry[1]))
                        M_lo.append(float(entry[2]))
                        M_hi.append(float(entry[3]))
                if line_i == N_bins:
                    parse_stats = False
                    line_i = 0 
            else:
                if line.startswith("# Totals:"):
                    parse_totals = True
                if line.startswith("# Statistics:"):
                    parse_totals = False
                    parse_stats = True

    density_color = "mediumturquoise"
    velocity_color = "teal"
    temperature_color = "lightsalmon"
    dust_color = "mediumvioletred"
    pressure_color = "lightcoral"
    entropy_color = "blueviolet"
    mach_color = "plum"
    linewidth = 2
    color_hot, color_mixed, color_cool = sns.color_palette(palette="flare", n_colors=3)
    styles = ["solid", "dashed", "dashdot", "dotted"]
    if phase == "hot":
        color = color_hot
    if phase == "cold":
        color = color_cool

    matplotlib.rcParams.update({'font.size': 15})

    if mode == "dark":
        plt.style.use('dark_background')

    bin_tot = np.array(bin_tot)
    m_gas = np.array(m_gas)
    m_dust_0 = np.array(m_dust_0)
    m_dust_1 = np.array(m_dust_1)
    m_dust_2 = np.array(m_dust_2)
    m_dust_3 = np.array(m_dust_3)
    m_dust = np.array([m_dust_0, m_dust_1, m_dust_2, m_dust_3])

    plt.semilogy(bin_tot[bin_tot>r_mask], m_gas[bin_tot>r_mask], c=color, linewidth=linewidth)
    # plt.title(rf"total {phase} gas mass, $t={round(time, 1)}$ Myr")
    plt.xlabel("r [kpc]")
    plt.ylabel(r"$m_{gas}$ $[M_\odot]$")
    # plt.ylim(1)
    plt.xlim(0, 10)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, f"{simulation}_{fnum}_gas_{phase}_total{tail}.png"), dpi=300)
    plt.close()

    for i, field in enumerate(field_names):
        plt.semilogy(bin_tot[bin_tot>r_mask], m_dust[i][bin_tot>r_mask], linewidth=linewidth, linestyle=styles[i], color=color)
        if simulation == "m82" and phase == "cold":
            if field == "dust_0":
                plt.plot(0, 0, label=r"1 $\mu$m", linestyle=styles[0], color="black", linewidth=linewidth)
            if field == "dust_1":
                plt.plot(0, 0, label=r"0.1 $\mu$m", linestyle=styles[1], color="black", linewidth=linewidth)
            if field == "dust_2":
                plt.plot(0, 0, label=r"0.01 $\mu$m", linestyle=styles[2], color="black", linewidth=linewidth)
            if field == "dust_3": 
                plt.plot(0, 0, label=r"0.001 $\mu$m", linestyle=styles[3], color="black", linewidth=linewidth)
            plt.legend(fontsize=13)
    # plt.title(rf"total dust mass, $t={round(time, 1)}$ Myr")
    # plt.ylim(1e-10, 1e3)
    plt.ylim(1, 6e5)
    plt.xlim(0, 10)
    plt.xlabel("r [kpc]")
    plt.ylabel(r"$m_{dust}$ $[M_\odot]$")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, f"{simulation}_{fnum}_dust_total_{phase}_{weight}{tail}.png"), dpi=300)
    plt.close()

    print(f"Total gas mass: {np.sum(m_gas[bin_tot>r_mask]):e} M_sun")
    print(f"Total 1 micron dust mass: {np.sum(m_dust_0[bin_tot>r_mask]):e} M_sun")
    print(f"Total 0.1 micron dust mass: {np.sum(m_dust_1[bin_tot>r_mask]):e} M_sun")
    print(f"Total 0.01 micron dust mass: {np.sum(m_dust_2[bin_tot>r_mask]):e} M_sun")
    print(f"Total 0.001 micron dust mass: {np.sum(m_dust_3[bin_tot>r_mask]):e} M_sun")

    def n_hot(r, n1):
        return n1 * r ** (-0.05 * r - 1.08)
    def n_cold(r, n1):
        return n1 * r ** -2
    
    fig, ax = plt.subplots(2, 3, figsize=(15, 7.5), sharex=True)

    ax[0][0].semilogy(bin_tot, gas_avg, c=color, label="avg", linewidth=linewidth)
    ax[0][0].semilogy(bin_tot, gas_med, c=color, label="med", linestyle="--", linewidth=linewidth)
    ax[0][0].fill_between(bin_tot, gas_lo, gas_hi, color=color, alpha=0.2)

    lopez_densities = [1.6, 0.8, 4.9, 3.7, 23, 7.9, 5.2, 5.1, 8.4, 4.6, 3.3, 2.6, 3.4, 2.6]  # cm^-3
    lopez_density_err = [0.1, 0.1, 0.2, 0.2, 0.4, 0.2, 0.3, 0.1, 0.15, 0.14, 0.1, 0.2, 0.2, 0.2]  # cm^-3
    lopez_distance = [2.08, 2.57, 0.88, 0.76, 0.48, 0.60, 0.69, 1.16, 1.05, 1.73, 1.69, 1.94, 1.87, 1.82]  # kpc

    if phase == "hot":
        ax[0][0].plot(bin_tot, n_hot(bin_tot, gas_med[np.where(bin_tot==1)[0][0]]), linewidth=linewidth, label=r"$n\propto r^f$, $f=−0.05r−1.08$", c="k")
    if phase == "cold":
        ax[0][0].plot(bin_tot, n_cold(bin_tot, gas_med[np.where(bin_tot==1)[0][0]]), linewidth=linewidth, label=r"$n\propto r^{-2}$", c="k")
        ax[0][0].errorbar(lopez_distance, lopez_densities, yerr=lopez_density_err, fmt="x", c="k", elinewidth=1, label="Lopez+2025")
    ax[0][0].legend(fontsize=13)
    ax[0][0].set_ylabel(r"$n_{gas}$ $[cm^{-3}]$")

    ax[0][1].semilogy(bin_tot, v_avg, c=color, linewidth=linewidth)
    ax[0][1].semilogy(bin_tot, v_med, c=color, linestyle="--", linewidth=linewidth)
    ax[0][1].fill_between(bin_tot, v_lo, v_hi, color=color, alpha=0.2)
    ax[0][1].set_ylabel(r"$v_{gas}$ $[km\,s^{-1}]$")

    ax[0][2].plot(bin_tot, np.log10(P_avg), c=color, label="avg", linewidth=linewidth)
    ax[0][2].plot(bin_tot, np.log10(P_med), c=color, label="med", linestyle="--", linewidth=linewidth)
    ax[0][2].fill_between(bin_tot, np.log10(P_lo), np.log10(P_hi), color=color, alpha=0.2)
    ax[0][2].set_ylabel(r"$P/k_B~[K~cm^{-3}]$")

    ax[1][0].plot(bin_tot, np.log10(temp_avg), c=color, label="avg", linewidth=linewidth)
    ax[1][0].plot(bin_tot, np.log10(temp_med), c=color, label="med", linestyle="--", linewidth=linewidth)
    ax[1][0].fill_between(bin_tot, np.log10(temp_lo), np.log10(temp_hi), color=color, alpha=0.2)
    ax[1][0].set_xlabel("r [kpc]")
    ax[1][0].set_ylabel(r"$\log(T_{gas}$ $[K]$)")

    ax[1][1].plot(bin_tot, M_avg, c=color, label="avg", linewidth=linewidth)
    ax[1][1].plot(bin_tot, M_med, c=color, label="med", linestyle="--", linewidth=linewidth)
    ax[1][1].fill_between(bin_tot, M_lo, M_hi, color=color, alpha=0.2)
    ax[1][1].set_xlabel("r [kpc]")
    ax[1][1].set_ylabel(r"$M$")

    ax[1][2].semilogy(bin_tot, S_avg, c=color, label="avg", linewidth=linewidth)
    ax[1][2].semilogy(bin_tot, S_med, c=color, label="med", linestyle="--", linewidth=linewidth)
    ax[1][2].fill_between(bin_tot, S_lo, S_hi, color=color, alpha=0.2)
    ax[1][2].set_xlabel("r [kpc]")
    ax[1][2].set_ylabel(r"$S/k_B~[K\,cm^{-3}]$")
    
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, f"{simulation}_{fnum}_{phase}_{weight}{tail}.png"), dpi=300)
    plt.close()


if __name__ == "__main__":
    args = read_cmdline()

    sys.path.insert(0, args.configdir)
    import hconfig

    basedir = args.basedir
    outdir = args.outdir
    fnum = args.fnum
    simulation = args.simulation
    phase = args.phase
    weight = args.weight
    tail = args.tail
    r_mask = args.rmask
    mode = args.mode
    field_names = args.field_names

    main(basedir, outdir, fnum, simulation, phase, weight, tail, r_mask, mode, field_names)
