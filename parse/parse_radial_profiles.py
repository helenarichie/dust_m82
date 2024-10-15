import sys
sys.path.insert(0, "/Users/helenarichie/GitHub/my_scripts/")
import os
import matplotlib.pyplot as plt
from hconfig import *
KB = 1.3806e-16  # Boltzmann constant, cm^2 g / s^2 K

fnum = 800
phase = "cold"
date = "2024-08-28"
N_bins = 80
weight = "vweight"

if date == "2024-08-28":
    f_name = f"{fnum}_prof_m82_{phase}_{weight}.txt"
if date == "2024-08-29":
    f_name = f"{fnum}_prof_highz_{phase}_{weight}.txt"

basedir = f"/Users/helenarichie/Desktop/{date}/profiles/post/"

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
linewidth = 1.75

bin_tot = np.array(bin_tot)

plt.semilogy(bin_tot, m_gas, c=density_color, linewidth=linewidth)
plt.title(f"total {phase} gas mass")
plt.xlabel("r [kpc]")
plt.ylabel(r"$m_{gas}$ $[M_\odot]$")
plt.savefig(os.path.join(basedir, "png", f"{fnum}_gas_{phase}_total.png"), dpi=300)
plt.close()

plt.semilogy(bin_tot, m_dust_0, linewidth=linewidth, label=r"1 $\mu$m")
plt.semilogy(bin_tot, m_dust_1, linewidth=linewidth, label=r"0.1 $\mu$m")
plt.semilogy(bin_tot, m_dust_2, linewidth=linewidth, label=r"0.01 $\mu$m")
plt.semilogy(bin_tot, m_dust_3, linewidth=linewidth, label=r"0.001 $\mu$m")
plt.legend()
plt.title("total dust mass")
plt.xlabel("r [kpc]")
plt.ylabel(r"$m_{dust}$ $[M_\odot]$")
plt.savefig(os.path.join(basedir, "png", f"{fnum}_dust_total_{phase}_{weight}.png"), dpi=300)
plt.close()

print(f"Total gas mass: {np.sum(m_gas):e} M_sun")
print(f"Total 1 micron dust mass: {np.sum(m_dust_0):e} M_sun")
print(f"Total 0.1 micron dust mass: {np.sum(m_dust_1):e} M_sun")
print(f"Total 0.01 micron dust mass: {np.sum(m_dust_2):e} M_sun")
print(f"Total 0.001 micron dust mass: {np.sum(m_dust_3):e} M_sun")

def n_hot(r, n1):
    return n1 * r ** (-0.05 * r - 1.08)
def n_cold(r, n1):
    return n1 * r ** -2

plt.semilogy(bin_tot, gas_avg, c=density_color, label="avg", linewidth=linewidth)
plt.semilogy(bin_tot, gas_med, c=density_color, label="med", linestyle="--", linewidth=linewidth)
plt.fill_between(bin_tot, gas_lo, gas_hi, color=density_color, alpha=0.2)

if phase == "hot":
    plt.plot(bin_tot, n_hot(bin_tot, gas_med[np.where(bin_tot==1)[0][0]]), linewidth=linewidth, label=r"$n\propto r^f$, $f=−0.05r−1.08$", c="k")
if phase == "cold":
    plt.plot(bin_tot, n_cold(bin_tot, gas_med[np.where(bin_tot==1)[0][0]]), linewidth=linewidth, label=r"$n\propto r^{-2}$", c="k")
plt.legend()
plt.title("gas number density")
plt.xlabel("r [kpc]")
plt.ylabel(r"$n_{gas}$ $[cm^{-3}]$")
plt.savefig(os.path.join(basedir, "png", f"{fnum}_gas_density_{phase}_{weight}.png"), dpi=300)
plt.close()

plt.semilogy(bin_tot, v_avg, c=velocity_color, label="avg", linewidth=linewidth)
plt.semilogy(bin_tot, v_med, c=velocity_color, label="med", linestyle="--", linewidth=linewidth)
plt.fill_between(bin_tot, v_lo, v_hi, color=velocity_color, alpha=0.2)
plt.legend()
plt.title("gas velocity")
plt.xlabel("r [kpc]")
plt.ylabel(r"$v_{gas}$ $[km\,s^{-1}]$")
plt.savefig(os.path.join(basedir, "png", f"{fnum}_gas_velocity_{phase}_{weight}.png"), dpi=300)
plt.close()

plt.plot(bin_tot, np.log10(P_avg), c=pressure_color, label="avg", linewidth=linewidth)
plt.plot(bin_tot, np.log10(P_med), c=pressure_color, label="med", linestyle="--", linewidth=linewidth)
plt.fill_between(bin_tot, np.log10(P_lo), np.log10(P_hi), color=pressure_color, alpha=0.2)
plt.legend()
plt.title("pressure")
plt.xlabel("r [kpc]")
plt.ylabel(r"$P/k_B~[K~cm^{-3}]$")
plt.savefig(os.path.join(basedir, "png", f"{fnum}_gas_pressure_{phase}_{weight}.png"), dpi=300)
plt.close()

plt.plot(bin_tot, np.log10(temp_avg), c=temperature_color, label="avg", linewidth=linewidth)
plt.plot(bin_tot, np.log10(temp_med), c=temperature_color, label="med", linestyle="--", linewidth=linewidth)
plt.fill_between(bin_tot, np.log10(temp_lo), np.log10(temp_hi), color=temperature_color, alpha=0.2)
# plt.ylim(3, 5)
plt.legend()
plt.title("gas temperature")
plt.xlabel("r [kpc]")
plt.ylabel(r"$\log(T_{gas}$ $[K]$)")
plt.savefig(os.path.join(basedir, "png", f"{fnum}_gas_temp_{phase}_{weight}.png"), dpi=300)
plt.close()

plt.plot(bin_tot, M_avg, c=mach_color, label="avg", linewidth=linewidth)
plt.plot(bin_tot, M_med, c=mach_color, label="med", linestyle="--", linewidth=linewidth)
plt.fill_between(bin_tot, M_lo, M_hi, color=mach_color, alpha=0.2)
# plt.ylim(3, 5)
plt.legend()
plt.title("Mach number")
plt.xlabel("r [kpc]")
plt.ylabel(r"$M$")
plt.savefig(os.path.join(basedir, "png", f"{fnum}_mach_{phase}_{weight}.png"), dpi=300)
plt.close()

plt.semilogy(bin_tot, S_avg, c=entropy_color, label="avg", linewidth=linewidth)
plt.semilogy(bin_tot, S_med, c=entropy_color, label="med", linestyle="--", linewidth=linewidth)
plt.fill_between(bin_tot, S_lo, S_hi, color=entropy_color, alpha=0.2)
plt.legend()
plt.title("entropy")
plt.xlabel("r [kpc]")
plt.ylabel(r"$S/k_B~[K\,cm^{-3}]$")
plt.savefig(os.path.join(basedir, "png", f"{fnum}_entropy_{phase}_{weight}.png"), dpi=300)
plt.close()