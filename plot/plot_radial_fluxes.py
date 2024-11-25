###############################
crc = False
frontier = False
mypc = True
###############################

import sys
if crc:
    sys.path.insert(0, "/ix/eschneider/helena/code/my_scripts/")
if mypc:
    sys.path.insert(0, "/Users/helenarichie/GitHub/my_scripts/")
from hconfig import *
import os
import matplotlib.pyplot as plt

fnum = 600
date = "2024-10-25"
N_bins = 80
r_mask = 0
tail = ""
time = fnum * 50 / 1e3

if date == "2024-08-28" or "2024-11-01":
    f_name = f"{fnum}_prof_m82_flux{tail}.txt"
if date == "2024-10-25":
    f_name = f"{fnum}_prof_highz_flux{tail}.txt"

basedir = f"/Users/helenarichie/Desktop/{date}/profiles/radial/"

bins = []
density_flux_hot = []
momentum_flux_hot = []
energy_flux_hot = []
density_flux_mixed = []
momentum_flux_mixed = []
energy_flux_mixed = []
density_flux_cool = []
momentum_flux_cool = []
energy_flux_cool = []
dust_0_flux_hot = []
dust_0_flux_mixed = []
dust_0_flux_cool = []
dust_1_flux_hot = []
dust_1_flux_mixed = []
dust_1_flux_cool = []
dust_2_flux_hot = []
dust_2_flux_mixed = []
dust_2_flux_cool = []
dust_3_flux_hot = []
dust_3_flux_mixed = []
dust_3_flux_cool = []

parse = False

with open(os.path.join(basedir, f_name)) as f:
    line_i = 0
    for line in f:
        if parse:
            line_i += 1
            line = line.strip(" ").rstrip("\n").split(",")
            bins.append(float(line[0]))
            # hot
            density_flux_hot.append(float(line[2]))
            momentum_flux_hot.append(float(line[3]))
            energy_flux_hot.append(float(line[4]))
            # mixed
            density_flux_mixed.append(float(line[6]))
            momentum_flux_mixed.append(float(line[7]))
            energy_flux_mixed.append(float(line[8]))
            # cool
            density_flux_cool.append(float(line[10]))
            momentum_flux_cool.append(float(line[11]))
            energy_flux_cool.append(float(line[12]))
            # dust_0
            dust_0_flux_hot.append(float(line[13]))
            dust_0_flux_mixed.append(float(line[14]))
            dust_0_flux_cool.append(float(line[15]))
            # dust_1
            dust_1_flux_hot.append(float(line[16]))
            dust_1_flux_mixed.append(float(line[17]))
            dust_1_flux_cool.append(float(line[18]))
            # dust_2
            dust_2_flux_hot.append(float(line[19]))
            dust_2_flux_mixed.append(float(line[20]))
            dust_2_flux_cool.append(float(line[21]))
            # dust_3
            dust_3_flux_hot.append(float(line[22]))
            dust_3_flux_mixed.append(float(line[23]))
            dust_3_flux_cool.append(float(line[24]))
        elif line.startswith("# Radial bin"):
            parse = True

bins = np.array(bins)
density_flux_hot = np.array(density_flux_hot)
density_flux_mixed = np.array(density_flux_mixed)
density_flux_cool = np.array(density_flux_cool)
energy_flux_hot = np.array(energy_flux_hot)
energy_flux_mixed = np.array(energy_flux_mixed)
energy_flux_cool = np.array(energy_flux_cool)
momentum_flux_hot = np.array(momentum_flux_hot)
momentum_flux_mixed = np.array(momentum_flux_mixed)
momentum_flux_cool = np.array(momentum_flux_cool)
dust_0_flux_hot = np.array(dust_0_flux_hot)
dust_0_flux_mixed = np.array(dust_0_flux_mixed)
dust_0_flux_cool = np.array(dust_0_flux_cool)

density_color = "mediumturquoise"
energy_color = "mediumorchid"
momentum_color = "palevioletred"
linewidth = 1.75
hot_style = "solid"
mixed_style = "dashed"
cool_style = "dashdot"

cool_color = "cornflowerblue"
mixed_color = "mediumseagreen"
hot_color = "red"
tot_color = "black"

plt.plot(bins[bins>r_mask], density_flux_hot[bins>r_mask], c=hot_color, linewidth=linewidth, label="hot")
plt.plot(bins[bins>r_mask], density_flux_mixed[bins>r_mask], c=mixed_color, linewidth=linewidth, label="mixed")
plt.plot(bins[bins>r_mask], density_flux_cool[bins>r_mask], c=cool_color, linewidth=linewidth, label="cool")
plt.plot(bins[bins>r_mask], density_flux_cool[bins>r_mask]+density_flux_mixed[bins>r_mask]+density_flux_hot[bins>r_mask], c=tot_color, linewidth=linewidth, label="tot")
plt.title(rf"$t={round(time, 1)}$ Myr")
plt.xlabel("r [kpc]")
plt.ylabel(r"$\dot{M}$ $[M_\odot\,yr^{-1}]$")
plt.legend()
plt.savefig(os.path.join(basedir, "png", f"{fnum}_density_flux{tail}.png"), dpi=300)
plt.close()

plt.plot(bins[bins>r_mask], momentum_flux_hot[bins>r_mask], c=hot_color, linewidth=linewidth, label="hot")
plt.plot(bins[bins>r_mask], momentum_flux_mixed[bins>r_mask], c=mixed_color, linewidth=linewidth, label="mixed")
plt.plot(bins[bins>r_mask], momentum_flux_cool[bins>r_mask], c=cool_color, linewidth=linewidth, label="cool")
plt.plot(bins[bins>r_mask], momentum_flux_cool[bins>r_mask]+momentum_flux_mixed[bins>r_mask]+momentum_flux_hot[bins>r_mask], c=tot_color, linewidth=linewidth, label="tot")
plt.title(rf"$t={round(time, 1)}$ Myr")
plt.xlabel("r [kpc]")
plt.ylabel(r"$\dot{p}$ $[M_\odot\,km\,s^{-1}\,yr^{-1}]$")
plt.legend()
plt.savefig(os.path.join(basedir, "png", f"{fnum}_momentum_flux{tail}.png"), dpi=300)
plt.close()

plt.semilogy(bins[bins>r_mask], energy_flux_hot[bins>r_mask], c=hot_color, linewidth=linewidth, label="hot")
plt.semilogy(bins[bins>r_mask], energy_flux_mixed[bins>r_mask], c=mixed_color, linewidth=linewidth, label="mixed")
plt.semilogy(bins[bins>r_mask], energy_flux_cool[bins>r_mask], c=cool_color, linewidth=linewidth, label="cool")
plt.semilogy(bins[bins>r_mask], energy_flux_cool[bins>r_mask]+energy_flux_mixed[bins>r_mask]+energy_flux_hot[bins>r_mask], c=tot_color, linewidth=linewidth, label="tot")
plt.title(rf"$t={round(time, 1)}$ Myr")
plt.xlabel("r [kpc]")
plt.ylabel(r"$\dot{E}$ $[erg\,s^{-1}]$")
plt.legend()
plt.savefig(os.path.join(basedir, "png", f"{fnum}_energy_flux{tail}.png"), dpi=300)
plt.close()

plt.plot(bins[bins>r_mask], dust_0_flux_hot[bins>r_mask], c=hot_color, linewidth=linewidth, label="hot")
plt.plot(bins[bins>r_mask], dust_0_flux_mixed[bins>r_mask], c=mixed_color, linewidth=linewidth, label="mixed")
plt.plot(bins[bins>r_mask], dust_0_flux_cool[bins>r_mask], c=cool_color, linewidth=linewidth, label="cool")
plt.plot(bins[bins>r_mask], dust_0_flux_cool[bins>r_mask]+dust_0_flux_mixed[bins>r_mask]+dust_0_flux_hot[bins>r_mask], c=tot_color, linewidth=linewidth, label="tot")
plt.title(rf"$t={round(time, 1)}$ Myr")
plt.xlabel("r [kpc]")
plt.ylabel(r"$\dot{M}$ $[M_\odot\,yr^{-1}]$")
plt.legend()
plt.savefig(os.path.join(basedir, "png", f"{fnum}_dust_0_flux{tail}.png"), dpi=300)
plt.close()