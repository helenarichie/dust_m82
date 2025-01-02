###############################
crc = False
frontier = False
mypc = True
###############################

from csv import writer
import sys
import seaborn as sns
import os
if crc:
    sys.path.insert(0, "/ix/eschneider/helena/code/my_scripts/")
if mypc:
    sys.path.insert(0, "/Users/helenarichie/GitHub/my_scripts/")
from hconfig import *

date = "2024-10-25"
no_disk = True
disk_i = 1
color_hot, color_mixed, color_cool = sns.color_palette(palette="flare", n_colors=3)
colors = [color_hot, color_mixed, color_cool]
styles = ["dashdot", "dotted", "dashed", "solid"]

########## data type ############
debugging = False
cloud_wind = False
testing = False
m82 = True
#################################

if crc:
  if debugging:
      basedir = f"/ix/eschneider/helena/data/debugging/{date}/"
  if cloud_wind:
      basedir = f"/ix/eschneider/helena/data/cloud_wind/{date}/"
  if testing:
      basedir = f"/ix/eschneider/helena/data/testing/{date}/"
  if m82:
      basedir = f"/ix/eschneider/helena/data/m82/{date}/"
if frontier:
  basedir = f"/lustre/orion/ast181/scratch/helenarichie/{date}/"
if mypc:
  basedir = f"/Users/helenarichie/Desktop/{date}/profiles/vertical/"

csvdir = os.path.join(basedir, "csv/")

d_arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
if no_disk:
    d_arr = d_arr[disk_i:]

fields = ["sputtered_0", "sputtered_1", "sputtered_2", "sputtered_3"]
labels = ["hot", "mixed", "cool"]

sputtered_0_hot = []
sputtered_1_hot = []
sputtered_2_hot = []
sputtered_3_hot = []
sputtered_0_mixed = []
sputtered_1_mixed = []
sputtered_2_mixed = []
sputtered_3_mixed = []
sputtered_0_cool = []
sputtered_1_cool = []
sputtered_2_cool = []
sputtered_3_cool = []

with open(os.path.join(csvdir, f"sputtered_0_hot_short.csv"), "r") as f:
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        sputtered_0_hot.append(line)
f.close()
sputtered_0_hot = np.array(sputtered_0_hot, dtype=float)

with open(os.path.join(csvdir, f"sputtered_1_hot_short.csv"), "r") as f:
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        sputtered_1_hot.append(line)
f.close()
sputtered_1_hot = np.array(sputtered_1_hot, dtype=float)

with open(os.path.join(csvdir, f"sputtered_2_hot_short.csv"), "r") as f:
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        sputtered_2_hot.append(line)
f.close()
sputtered_2_hot = np.array(sputtered_2_hot, dtype=float)

with open(os.path.join(csvdir, f"sputtered_3_hot_short.csv"), "r") as f:
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        sputtered_3_hot.append(line)
f.close()
sputtered_3_hot = np.array(sputtered_3_hot, dtype=float)

with open(os.path.join(csvdir, f"sputtered_0_mixed_short.csv"), "r") as f:
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        sputtered_0_mixed.append(line)
f.close()
sputtered_0_mixed = np.array(sputtered_0_mixed, dtype=float)

with open(os.path.join(csvdir, f"sputtered_1_mixed_short.csv"), "r") as f:
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        sputtered_1_mixed.append(line)
f.close()
sputtered_1_mixed = np.array(sputtered_1_mixed, dtype=float)

with open(os.path.join(csvdir, f"sputtered_2_mixed_short.csv"), "r") as f:
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        sputtered_2_mixed.append(line)
f.close()
sputtered_2_mixed = np.array(sputtered_2_mixed, dtype=float)

with open(os.path.join(csvdir, f"sputtered_3_mixed_short.csv"), "r") as f:
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        sputtered_3_mixed.append(line)
f.close()
sputtered_3_mixed = np.array(sputtered_3_mixed, dtype=float)

with open(os.path.join(csvdir, f"sputtered_0_cool_short.csv"), "r") as f:
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        sputtered_0_cool.append(line)
f.close()
sputtered_0_cool = np.array(sputtered_0_cool, dtype=float)

with open(os.path.join(csvdir, f"sputtered_1_cool_short.csv"), "r") as f:
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        sputtered_1_cool.append(line)
f.close()
sputtered_1_cool = np.array(sputtered_1_cool, dtype=float)

with open(os.path.join(csvdir, f"sputtered_2_cool_short.csv"), "r") as f:
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        sputtered_2_cool.append(line)
f.close()
sputtered_2_cool = np.array(sputtered_2_cool, dtype=float)

with open(os.path.join(csvdir, f"sputtered_3_cool_short.csv"), "r") as f:
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        sputtered_3_cool.append(line)
f.close()
sputtered_3_cool = np.array(sputtered_3_cool, dtype=float)
        
for i, x in enumerate(sputtered_0_hot):
    fig, ax = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
    # ymin, ymax = 1, 5e7
    ymin, ymax = 1, 5e5
    linewidth = 3
    time = sputtered_0_hot[i][0]
    #plt.stairs(sputtered_0_hot[i][disk_i+1:], d_arr, linewidth=linewidth, color=colors[0], linestyle=styles[0])
    # disk_i + 1 because the 0th index is the simulation time
    ax[0].stairs(sputtered_1_hot[i][disk_i+1:], d_arr, linewidth=linewidth, color=colors[0], linestyle=styles[1])
    ax[0].stairs(sputtered_2_hot[i][disk_i+1:], d_arr, linewidth=linewidth, color=colors[0], linestyle=styles[2])
    ax[0].stairs(sputtered_3_hot[i][disk_i+1:], d_arr, linewidth=linewidth, color=colors[0], linestyle=styles[3])
    # plt.title(f"$t={round(time/1e3, 1)}$ Myr")
    ax[0].tick_params(axis='both', which="both", labelsize=15, top=True, right=True)
    ax[0].set_yscale('log')
    ax[0].set_ylabel(r"$m_{sput}~[M_\odot]$", fontsize=20)
    ax[0].set_xlabel(r"$z~[kpc]$", fontsize=20)
    ax[0].set_xlim(np.amin(d_arr), np.amax(d_arr))
    ax[0].set_ylim(ymin, ymax)

    #plt.stairs(sputtered_0_mixed[i][disk_i+1:], d_arr, linewidth=linewidth, color=colors[1], linestyle=styles[0])
    ax[1].stairs(sputtered_1_mixed[i][disk_i+1:], d_arr, linewidth=linewidth, color=colors[1], linestyle=styles[1])
    ax[1].stairs(sputtered_2_mixed[i][disk_i+1:], d_arr, linewidth=linewidth, color=colors[1], linestyle=styles[2])
    ax[1].stairs(sputtered_3_mixed[i][disk_i+1:], d_arr, linewidth=linewidth, color=colors[1], linestyle=styles[3])
    # plt.title(f"$t={round(time/1e3, 1)}$ Myr")
    ax[1].tick_params(axis='both', which="both", labelsize=15, top=True, right=True)
    ax[1].set_yscale('log')
    ax[1].set_xlabel(r"$z~[kpc]$", fontsize=20)
    ax[1].set_xlim(np.amin(d_arr), np.amax(d_arr))
    ax[1].set_ylim(ymin, ymax)

    #plt.plot(0, 0, linestyle=styles[0], label=r"$a=1~\mu$m", c="k", linewidth=linewidth)
    ax[2].plot(0, 0, linestyle=styles[1], label=r"$a=0.1~\mu$m", c="k", linewidth=linewidth)
    ax[2].plot(0, 0, linestyle=styles[2], label=r"$a=0.01~\mu$m", c="k", linewidth=linewidth)
    ax[2].plot(0, 0, linestyle=styles[3], label=r"$a=0.001~\mu$m", c="k", linewidth=linewidth)
    # plt.plot(0, 0, c=colors[2], linewidth=linewidth, label=labels[2])
    #plt.stairs(sputtered_0_cool[i][disk_i+1:], d_arr, linewidth=linewidth, color=colors[2], linestyle=styles[0])
    ax[2].stairs(sputtered_1_cool[i][disk_i+1:], d_arr, linewidth=linewidth, color=colors[2], linestyle=styles[1])
    ax[2].stairs(sputtered_2_cool[i][disk_i+1:], d_arr, linewidth=linewidth, color=colors[2], linestyle=styles[2])
    ax[2].stairs(sputtered_3_cool[i][disk_i+1:], d_arr, linewidth=linewidth, color=colors[2], linestyle=styles[3])
    # plt.title(f"$t={round(time/1e3, 1)}$ Myr")
    ax[2].tick_params(axis='both', which="both", labelsize=15, top=True, right=True)
    ax[2].set_yscale('log')
    ax[2].set_xlabel(r"$z~[kpc]$", fontsize=20)
    ax[2].set_xlim(np.amin(d_arr), np.amax(d_arr))
    ax[2].set_ylim(ymin, ymax)
    ax[2].legend(fontsize=15)

    plt.tight_layout()
    plt.savefig(os.path.join(basedir, "png", "sputtered", f"{int(time/500)}.png"), dpi=300)
    plt.close()