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
    p.add_argument("-p", "--phase", type=str, required=True)
    p.add_argument("-w", "--weight", type=str, required=True)
    p.add_argument("-t", "--tail", type=str, required=False, default="")
    p.add_argument("-r", "--rmask", type=int, required=False, default=0)
    p.add_argument("-m", "--mode", type=str, choices=["dark", "light"], required=False, default="light")
    args = p.parse_args()
    return args

def main(basedir, fnum, simulation, phase, weight, tail, r_mask, mode):
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

    wh_bin = np.where(bins == 1)[0]

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

    if mode == "dark":
        plt.style.use('dark_background')

    bin_tot = np.array(bin_tot)
    m_gas = np.array(m_gas)
    m_dust_0 = np.array(m_dust_0)
    m_dust_1 = np.array(m_dust_1)
    m_dust_2 = np.array(m_dust_2)
    m_dust_3 = np.array(m_dust_3)

    plt.semilogy(bin_tot[bin_tot>r_mask], m_dust_0[bin_tot>r_mask]/dust_0_rate_cool[wh_bin], linewidth=linewidth, label=r"1 $\mu$m", linestyle=styles[0], color=color)
    plt.semilogy(bin_tot[bin_tot>r_mask], m_dust_1[bin_tot>r_mask]/dust_1_rate_cool[wh_bin], linewidth=linewidth, label=r"0.1 $\mu$m", linestyle=styles[1], color=color)
    plt.semilogy(bin_tot[bin_tot>r_mask], m_dust_2[bin_tot>r_mask]/dust_2_rate_cool[wh_bin], linewidth=linewidth, label=r"0.01 $\mu$m", linestyle=styles[2], color=color)
    plt.semilogy(bin_tot[bin_tot>r_mask], m_dust_3[bin_tot>r_mask]/dust_3_rate_cool[wh_bin], linewidth=linewidth, label=r"0.001 $\mu$m", linestyle=styles[3], color=color)
    plt.legend()
    plt.title(rf"normalized, ${round(time, 1)}$ Myr")
    # plt.ylim(1e-10, 1e3)
    plt.xlabel("r [kpc]")
    plt.ylabel(r"$m_{dust}/\dot{m}_{dust,r=1}$")
    plt.savefig(os.path.join(basedir, "png", f"{fnum}_dust_total_norm_{phase}_{weight}{tail}.png"), dpi=300)
    plt.close()


    plt.semilogy(bin_tot[bin_tot>r_mask], dust_0_rate_cool[bin_tot>r_mask]/dust_0_rate_cool[wh_bin], linewidth=linewidth, label=r"1 $\mu$m", linestyle=styles[0], color=color)
    plt.semilogy(bin_tot[bin_tot>r_mask], dust_1_rate_cool[bin_tot>r_mask]/dust_1_rate_cool[wh_bin], linewidth=linewidth, label=r"0.1 $\mu$m", linestyle=styles[1], color=color)
    plt.semilogy(bin_tot[bin_tot>r_mask], dust_2_rate_cool[bin_tot>r_mask]/dust_2_rate_cool[wh_bin], linewidth=linewidth, label=r"0.01 $\mu$m", linestyle=styles[2], color=color)
    plt.semilogy(bin_tot[bin_tot>r_mask], dust_3_rate_cool[bin_tot>r_mask]/dust_3_rate_cool[wh_bin], linewidth=linewidth, label=r"0.001 $\mu$m", linestyle=styles[3], color=color)
    plt.legend()
    plt.title(rf"normalized, ${round(time, 1)}$ Myr")
    # plt.ylim(1e-10, 1e3)
    plt.xlabel("r [kpc]")
    plt.ylabel(r"$\dot{m}_{dust}/\dot{m}_{dust,r=1}$")
    plt.savefig(os.path.join(basedir, "png", f"{fnum}_dust_rate_norm_{phase}_{weight}{tail}.png"), dpi=300)
    plt.close()

    plt.semilogy(bin_tot[bin_tot>r_mask], dust_0_rate_cool[bin_tot>r_mask], linewidth=linewidth, label=r"1 $\mu$m", linestyle=styles[0], color=color)
    plt.semilogy(bin_tot[bin_tot>r_mask], dust_1_rate_cool[bin_tot>r_mask], linewidth=linewidth, label=r"0.1 $\mu$m", linestyle=styles[1], color=color)
    plt.semilogy(bin_tot[bin_tot>r_mask], dust_2_rate_cool[bin_tot>r_mask], linewidth=linewidth, label=r"0.01 $\mu$m", linestyle=styles[2], color=color)
    plt.semilogy(bin_tot[bin_tot>r_mask], dust_3_rate_cool[bin_tot>r_mask], linewidth=linewidth, label=r"0.001 $\mu$m", linestyle=styles[3], color=color)
    plt.legend()
    plt.title(rf"outflow rate, ${round(time, 1)}$ Myr")
    # plt.ylim(1e-10, 1e3)
    plt.xlabel("r [kpc]")
    plt.ylabel(r"$\dot{m}_{dust}$")
    plt.savefig(os.path.join(basedir, "png", f"{fnum}_dust_rate_{phase}_{weight}{tail}.png"), dpi=300)
    plt.close()

    print(f"Total gas mass: {np.sum(m_gas[bin_tot>r_mask]):e} M_sun")
    print(f"Total 1 micron dust mass: {np.sum(m_dust_0[bin_tot>r_mask]):e} M_sun")
    print(f"Total 0.1 micron dust mass: {np.sum(m_dust_1[bin_tot>r_mask]):e} M_sun")
    print(f"Total 0.01 micron dust mass: {np.sum(m_dust_2[bin_tot>r_mask]):e} M_sun")
    print(f"Total 0.001 micron dust mass: {np.sum(m_dust_3[bin_tot>r_mask]):e} M_sun")


if __name__ == "__main__":
    args = read_cmdline()

    sys.path.insert(0, args.configdir)
    import hconfig

    basedir = args.basedir
    fnum = args.fnum
    simulation = args.simulation
    phase = args.phase
    weight = args.weight
    tail = args.tail
    r_mask = args.rmask
    mode = args.mode

    main(basedir, fnum, simulation, phase, weight, tail, r_mask, mode)
