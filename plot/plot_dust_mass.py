import sys
sys.path.insert(0, "/ix/eschneider/helena/code/my_scripts/")
from hconfig import *

density_conversion = 5.028e-34/(3.24e-22)**3 # g/cm^3 to M_sun/kpc^3

plt.rcParams.update({'font.family': 'Helvetica'})
fontsize = 25
plt.rcParams.update({'font.size': fontsize})

##################################################################
date = "2024-07-07"
cat = True
pad = 0.1
labelpad = 12
linewidth = 5.5
tickwidth = 1
##################################################################

tmax = 100e6

##################################################################
basedir = f"/ix/eschneider/helena/data/m82/{date}/"
pngdir = os.path.join(basedir, "png/")
csvdir = os.path.join(basedir, "csv/")
##################################################################

time = []
with open(os.path.join(csvdir, "time.csv")) as f:
    for line in f:
        time.append(float(line))
time = np.array(time)

sputter_hot = []
with open(os.path.join(csvdir, "sputter_hot.csv")) as f:
    for line in f:
        sputter_hot.append(float(line))

sputter = []
with open(os.path.join(csvdir, "sputter.csv")) as f:
    for line in f:
        sputter.append(float(line))

sputter_tot, sputter_tot_hot = [], []
mass_cumulative, mass_cumulative_hot = 0, 0
for i, mass in enumerate(sputter):
    mass_cumulative += mass
    mass_cumulative_hot += sputter_hot[i]
    sputter_tot.append(mass_cumulative)
    sputter_tot_hot.append(mass_cumulative_hot)
sputter_tot = np.array(sputter_tot)
sputter_tot_hot = np.array(sputter_tot_hot)

ymin = 0
ymax = np.amax([np.amax(sputter_tot_hot), np.amax(sputter_tot)]) + pad
xmin = np.amin(time[time<=tmax]) - pad
xmax = np.amax(time[time<=tmax]) + pad

fig = plt.figure(figsize=(9.9, 7.75))
old = "#C53f91"
new = "#d43a4f"
plt.plot(time[time<=tmax]/1e3, (sputter_tot[time<=tmax]+sputter_tot_hot[time<=tmax]), c="k", label=r"sputtered", linewidth=linewidth, zorder=1)
plt.plot(time[time<=tmax]/1e3, sputter_tot[time<=tmax], c="k", linestyle="--", linewidth=linewidth-2, zorder=1, label=r"$T<10^6~K$")
plt.plot(time[time<=tmax]/1e3, sputter_tot_hot[time<=tmax], c="k", linestyle="-.", linewidth=linewidth-2, zorder=1, label=r"$T\geq10^6~K$")
plt.legend(fontsize=23, loc="upper left")
plt.xlim(xmin/1e3, xmax/1e3)
plt.tick_params(axis='both', which='both', direction='in', color='black', top=1, right=1, length=9, width=2, reset=True)
plt.xticks(np.linspace(0, xmax/1e3, 5).round(1))
plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
plt.xlabel("Time [Myr]", fontsize=fontsize+3)
plt.ylabel(r"$m_{dust}~[M_\odot]$", fontsize=fontsize+5)
plt.tight_layout()
plt.savefig(pngdir + f"dust_mass_{date}.png", dpi=300, bbox_inches="tight")

print("Final total sputtered mass: ", (sputter_tot[time<=tmax][-1]+sputter_tot_hot[time<=tmax][-1]))
print("Final hot phase sputtered mass: ", (sputter_tot_hot[time<=tmax][-1]))
print("Final cool phase sputtered mass: ", (sputter_tot[time<=tmax][-1]))