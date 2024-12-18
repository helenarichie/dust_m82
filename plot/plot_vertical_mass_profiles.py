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

date = "2024-10-25"
tmaxs = np.linspace(0, 50000, 101)

substr = "dust_3"
# ymax = 4e8  # high-z gas
ymax = 3e6  # high-z dust
# ymax = 2e4  # m82 dust
no_disk = True
disk_i = 1

########## data type ############
debugging = False
cloud_wind = False
testing = False
m82 = False
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

labels = ["hot", "mixed", "cool"]

breakout = False
tmax_i = 0
with open(os.path.join(csvdir, f"{substr}.csv")) as f:
    for line in f:
        line = line.split(",")
        masses = np.zeros((10, 3))
        for i, bin in enumerate(line):
            bin = bin.replace("[", "")
            bin = bin.replace("]", "")
            bin = bin.split(" ")
            while("" in bin):
                bin.remove("")
            if i < 10:  # should be unneccessary, I should be 0-9, just checking there there's less than 10 bins
                masses[i] = np.array(bin[1:4], dtype=float)  # 1:4 = hot, mixed, cold (excludes 0, which is time)
        if float(bin[0]) == tmaxs[tmax_i]:
            for j in range(0, 2+1):
                if no_disk:
                    plt.stairs(masses[:,j][disk_i:], d_arr, label=labels[j] + rf", total = {np.sum(masses[:,j][disk_i:]):.1e} $M_\odot$", linewidth=2)
                    print(f"{labels[j]} {substr} total mass at {round(tmaxs[tmax_i]/1e3, 1):.2e} Myr: {np.sum(masses[:,j][disk_i:]):.1e} M_sun")
                else:
                    plt.stairs(masses[:,j], d_arr, label=labels[j] + rf", total = {np.sum(masses[:,j]):.1e} $M_\odot$", linewidth=2)
            print("\n")
            plt.title(f"{substr} mass, $t={round(tmaxs[tmax_i]/1e3, 1)}$ Myr")
            plt.yscale('log')
            plt.ylabel(r"$log_{10}(M~[M_\odot])$")
            plt.xlabel(r"$r~[kpc]$")
            plt.ylim(10, ymax)
            plt.legend()
            plt.tick_params(top=True, right=True, which="both")
            if mypc:
                plt.savefig(os.path.join(basedir, "png", substr, f"{int(tmaxs[tmax_i]/500)}_{substr}.png"), dpi=300)
            else:
                plt.savefig(f"../png/{substr}/{int(tmaxs[tmax_i]/1e3)/500}_{substr}.png", dpi=300)
            plt.close()

            if tmax_i < (len(tmaxs)-1):
                tmax_i += 1
            # if you're at the end of the tmaxs array, break out of the loop and end the program
            else:
                breakout = True
                break
        
        if breakout:
            break