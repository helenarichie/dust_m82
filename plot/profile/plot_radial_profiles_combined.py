import argparse
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import sys


def read_cmdline():
    p = argparse.ArgumentParser()
    p.add_argument("-b", "--basedir", type=str, required=True)
    p.add_argument("-c", "--configdir", type=str, required=True)
    p.add_argument("-o", "--outdir", type=str, required=True)
    p.add_argument("-f", "--fnum", type=int, required=True)
    p.add_argument("-s", "--simulation", type=str, required=True)
    p.add_argument("-p", "--phase", type=str, required=True)
    p.add_argument("-w", "--weight", type=str, required=True)
    p.add_argument("-t", "--tail", type=str, required=False, default="")
    p.add_argument("-r", "--rmask", type=int, required=False, default=0)
    p.add_argument("-m", "--mode", type=str, choices=["dark", "light"], required=False, default="light")
    args = p.parse_args()
    return args

def main(basedir, outdir, fnum, simulation, phase, weight, tail, r_mask, mode):
    N_bins = 80
    time = fnum * 50 / 1e3
    linewidth = 2
    # color = line_color = "#00581c"
    color = line_color = "k"

    f_name = f"{fnum}_prof_{simulation}_{phase}_{weight}{tail}.txt"

    filedirs = [os.path.join(basedir, f_name), os.path.join("/Users/helenarichie/Desktop/2024-10-25/profiles/radial/", f"{fnum}_prof_highz_{phase}_{weight}{tail}.txt")]

    fig, ax = plt.subplots(4, 1, figsize=(7, 15), sharex=True, gridspec_kw={"hspace":0})

    mean_linestyle = ":"
    med_linestyle = "--"

    ax = ax.flat

    change_color = False

    for ax_i in ax:
        ax_i.set_xlim(0, 10)

    if phase == "hot":
        ax[0].plot(-1, 1e-2, label=r"$n\propto r^f$, $f=−0.05r−1.08$", c="k", linewidth=linewidth)
        ax[0].plot(-1, 1e-2, label=r"mean", c="k", linestyle=mean_linestyle, linewidth=linewidth)
        ax[0].plot(-1, 1e-2, label=r"med", c="k", linestyle=med_linestyle, linewidth=linewidth)
    if phase == "cold":
        ax[0].plot(-1, 1, label=r"$n\propto r^{-2}$", c="k", linewidth=linewidth)
        ax[0].plot(-1, 1, label=r"mean", c="k", linestyle=mean_linestyle, linewidth=linewidth)
        ax[0].plot(-1, 1, label=r"med", c="k", linestyle=med_linestyle, linewidth=linewidth)


    for filedir in filedirs:

        if change_color:
            # color = "#a1caff"
            # line_color = "steelblue"
            color = "orchid"
            line_color = color
        
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

        with open(filedir) as f:
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
                        if i == 8:
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


        fontsize=17
        matplotlib.rcParams.update({'font.size': fontsize})

        if mode == "dark":
            plt.style.use('dark_background')

        def n_hot(r, n1):
            return n1 * r ** (-0.05 * r - 1.08)
        def n_cold(r, n1):
            return n1 * r ** -2
        
        bin_tot = np.array(bin_tot)

        ax[0].legend(fontsize=fontsize)

        ax[0].semilogy(bin_tot, gas_avg, c=line_color, linewidth=linewidth, linestyle=mean_linestyle)
        ax[0].semilogy(bin_tot, gas_med, c=line_color, linestyle=med_linestyle, linewidth=linewidth)
        ax[0].fill_between(bin_tot, gas_lo, gas_hi, color=color, alpha=0.2)
        ax[0].tick_params(axis='both', which="both", labelsize=fontsize-2, top=True, right=True)

        pad = 5.5
        if phase == "hot":
            ax[0].plot(bin_tot, n_hot(bin_tot, gas_med[np.where(bin_tot==1)[0][0]]), linewidth=linewidth, c=line_color)
            ax[0].set_title(r"$T\geq5\times10^5~K$", pad=pad)
        if phase == "cold":
            ax[0].plot(bin_tot, n_cold(bin_tot, gas_med[np.where(bin_tot==1)[0][0]]), linewidth=linewidth, c=line_color)
            ax[0].set_title(r"$T\leq2\times10^4~K$", pad=pad)

        ax[0].set_ylabel(r"$n_{gas}$ $[cm^{-3}]$", fontsize=fontsize)

        ax[1].semilogy(bin_tot, v_avg, c=line_color, linewidth=linewidth, linestyle=mean_linestyle)
        ax[1].semilogy(bin_tot, v_med, c=line_color, linestyle=med_linestyle, linewidth=linewidth)
        ax[1].fill_between(bin_tot, v_lo, v_hi, color=color, alpha=0.2)
        ax[1].set_ylabel(r"$v_{r}$ $[km\,s^{-1}]$", fontsize=fontsize)
        ax[1].set_ylim(9, 2e3)
        ax[1].tick_params(axis='both', which="both", labelsize=fontsize-2, top=True, right=True)

        ax[2].plot(bin_tot, np.log10(P_avg), c=line_color, linewidth=linewidth, linestyle=mean_linestyle)
        ax[2].plot(bin_tot, np.log10(P_med), c=line_color, linestyle=med_linestyle, linewidth=linewidth)
        ax[2].fill_between(bin_tot, np.log10(P_lo), np.log10(P_hi), color=color, alpha=0.2)
        ax[2].set_ylabel(r"$P/k_B~[K~cm^{-3}]$", fontsize=fontsize)
        ax[2].set_ylim(0.5, 6.2)
        ax[2].tick_params(axis='both', which="both", labelsize=fontsize-2, top=True, right=True)

        ax[3].plot(bin_tot, np.log10(temp_avg), c=line_color, linewidth=linewidth, linestyle=mean_linestyle)
        ax[3].plot(bin_tot, np.log10(temp_med), c=line_color, label="med", linestyle=med_linestyle, linewidth=linewidth)
        ax[3].fill_between(bin_tot, np.log10(temp_lo), np.log10(temp_hi), color=color, alpha=0.2)
        ax[3].set_xlabel("r [kpc]", fontsize=fontsize)
        ax[3].set_ylabel(r"$\log(T$ $[K]$)", fontsize=fontsize)
        # ax[3].set_ylim(3.25, 7.3)
        ax[3].tick_params(axis='both', which="both", labelsize=fontsize-2, top=True, right=True)

        change_color = True
    
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, f"{phase}_radial_profile.png"), dpi=300)
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

    main(basedir, outdir, fnum, simulation, phase, weight, tail, r_mask, mode)
