import sys
sys.path.insert(0, "/ix/eschneider/helena/code/my_scripts/")
from hconfig import *

date = "2024-08-28"
tmaxs = np.linspace(0, 50) * 1e3
sputtered_substr = "sputtered_3"

###############################
crc = True
frontier = False
###############################

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

csvdir = os.path.join(basedir, "csv/")

sputtered = np.zeros((10, 3))
d_arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
labels = ["hot", "mixed", "cool"]

breakout = False
tmax_i = 0
with open(os.path.join(csvdir, f"{sputtered_substr}.csv")) as f:
    for line in f:
        line = line.split(",")
        for i, bin in enumerate(line):
            bin = bin.replace("[", "")
            bin = bin.replace("]", "")
            bin = bin.split(" ")
            while("" in bin):
                bin.remove("")
            if i < 10:
                sputtered[i] = sputtered[i] + np.array(bin[1:4], dtype=float)
            if float(bin[0]) <= tmaxs[tmax_i]:
                continue
            else:
                print(float(bin[0]))
                for j in range(0, 2+1):
                    #plt.plot(d_arr[:-1], np.log10(sputtered_0[:,i]), label=labels[i-1])
                    plt.stairs(sputtered[:,j], d_arr, label=labels[j])

                plt.title(f"cumulative sputtered mass, $t={round(tmaxs[tmax_i]/1e3, 1)}$ Myr")
                plt.yscale('log')
                plt.ylabel(r"$log_{10}(M~[M_\odot])$")
                plt.xlabel(r"$r~[kpc]$")
                plt.ylim(1e-6, 1.5e6)
                plt.legend()
                plt.savefig(f"../png/{int(tmaxs[tmax_i]/1e3)}_{sputtered_substr}.png", dpi=300)
                plt.close()

                if tmax_i < (len(tmaxs)-1):
                    tmax_i += 1
                else:
                    breakout = True
                    break
        if breakout:
            break