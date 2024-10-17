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

date = "2024-08-28"
tmaxs = np.linspace(0, 51) * 1e3
substr = "dtg_3"
dust_substr = "dust_3"
no_disk = True

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
  basedir = f"/Users/helenarichie/Desktop/{date}/profiles/in_situ/"

csvdir = os.path.join(basedir, "csv/")

dtgr = np.zeros((10, 3))
if no_disk:
    d_arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
else:
    d_arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
labels = ["hot", "mixed", "cool"]

breakout = False
tmax_i = 0
with open(os.path.join(csvdir, "gas.csv")) as f1, open(os.path.join(csvdir, f"{dust_substr}.csv")) as f2:
    for line1, line2 in zip(f1, f2):
        line1 = line1.split(",")
        line2 = line2.split(",")
        for i, (bin1, bin2) in enumerate(zip(line1, line2)):
            bin1 = bin1.replace("[", "")
            bin1 = bin1.replace("]", "")
            bin1 = bin1.split(" ")
            bin2 = bin2.replace("[", "")
            bin2 = bin2.replace("]", "")
            bin2 = bin2.split(" ")
            while("" in bin1):
                bin1.remove("")
            while("" in bin2):
                bin2.remove("")
            if i < 10:
                dtgr[i] = np.array(bin2[1:4],dtype=float)/np.array(bin1[1:4], dtype=float)
            if float(bin1[0]) <= tmaxs[tmax_i]:
                continue
            else:
                for j in range(0, 2+1):
                    if no_disk:
                        plt.stairs(dtgr[:,j][1:], d_arr, label=labels[j], linewidth=2)
                    else:
                        plt.stairs(dtgr[:,j], d_arr, label=labels[j], linewidth=2)

                plt.title(f"dust to gas ratio, {dust_substr}, $t={round(tmaxs[tmax_i]/1e3, 1)}$ Myr")
                plt.yscale('log')
                plt.ylabel(r"$m_\mathrm{dust}/m_\mathrm{gas}$")
                plt.xlabel(r"$r~[kpc]$")
                plt.ylim(1e-3, 1.5e-2)
                plt.legend(loc="upper right")
                if mypc:
                    plt.savefig(os.path.join(basedir, "no_disk", substr, f"{int(tmaxs[tmax_i]/1e3)}_{substr}.png"), dpi=300)
                else:
                    plt.savefig(f"../png/{substr}/{int(tmaxs[tmax_i]/1e3)}_{substr}.png", dpi=300)
                plt.close()

                if tmax_i < (len(tmaxs)-1):
                    tmax_i += 1
                else:
                    breakout = True
                    break
        if breakout:
            break