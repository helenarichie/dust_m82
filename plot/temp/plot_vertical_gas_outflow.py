import sys
sys.path.insert(0, "/Users/helenarichie/GitHub/my_scripts/")
from hconfig import *

density_conversion = 5.028e-34/(3.24e-22)**3 # g/cm^3 to M_sun/kpc^3

plt.rcParams.update({'font.family': 'Helvetica'})
fontsize = 20
plt.rcParams.update({'font.size': fontsize})

date = "2024-10-25"
field = "cloud"

if date == "2024-08-28":
    name = "m82"
if (date == "2024-08-29") or (date == "2024-10-25"):
    name = "high-z"

##################################################################
basedir = f"/Users/helenarichie/Desktop/{date}/fluxes/"
pngdir = os.path.join(basedir, "png/")
csvdir = os.path.join(basedir, "csv/")
##################################################################

rate = []
with open(os.path.join(csvdir, f"rate_{field}_1e-24.csv")) as f:
    for line in f:
        line = line.split(",")
        rate.append(np.array(line, dtype=float))

time_output = []
with open(os.path.join(csvdir, "time_output_1e-24.csv")) as f:
    for line in f:
        time_output.append(float(line))
time_output = np.array(time_output)

dt_out = time_output[2] - time_output[1]

mass_out = []
mass_cumulative = 0
for i, rate_i in enumerate(rate):
    rate_i = np.sum(rate_i)
    mass_cumulative += rate_i * dt_out
    mass_out.append(mass_cumulative)
mass_out = np.array(mass_out)

fig = plt.figure(figsize=(9.9, 7.75))

##################################################################
pad = 10
linewidth = 5.5
##################################################################

ymin = np.amin(mass_out) - pad
ymax = np.amax(mass_out) + pad
xmin = np.amin(time_output) - pad
xmax = np.amax(time_output) + pad

if (field == "dust_0") or (field == "dust_1") or (field == "dust_2") or (field == "dust_3"):
    color = "#d43a4f"
if field == "cloud":
    color = "#49b4ab"

plt.semilogy(time_output/1e3, mass_out, linewidth=linewidth-1, c=color, zorder=0, label="exited box")
# plt.legend(fontsize=23)
# plt.xlim(xmin/1e3, xmax/1e3)
plt.tick_params(axis='both', which='both', direction='in', color='black', top=1, right=1, length=9, width=2, reset=True)
# plt.xticks(np.linspace(0, xmax/1e3, 5).round(1))
# plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
plt.xlabel("Time [Myr]", fontsize=fontsize+3)
plt.ylabel(rf"Mass $[M_\odot]$", fontsize=fontsize+5)
plt.title(f"{name} total {field} mass out: {np.sum(mass_out):.1e} $M_\odot$", fontsize=fontsize+5)
plt.tight_layout()
plt.savefig(pngdir + f"fluxes_{name}_{field}.png", dpi=300, bbox_inches="tight")
plt.close()

fig = plt.figure(figsize=(9.9, 7.75))

plt.plot(time_output/1e3, np.sum(rate, axis=1), linewidth=linewidth-1, c=color, zorder=0, label="exited box")
# plt.legend(fontsize=23)
# plt.xlim(xmin/1e3, xmax/1e3)
plt.tick_params(axis='both', which='both', direction='in', color='black', top=1, right=1, length=9, width=2, reset=True)
# plt.xticks(np.linspace(0, xmax/1e3, 5).round(1))
# plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
plt.xlabel("Time [Myr]", fontsize=fontsize+3)
plt.ylabel(rf"Outflow rate $[M_\odot\,yr^{-1}]$", fontsize=fontsize+5)
plt.title(f"{name} total {field} mass out: {np.sum(mass_out):.1e} $M_\odot$", fontsize=fontsize+5)
plt.tight_layout()
plt.savefig(pngdir + f"rates_{name}_{field}.png", dpi=300, bbox_inches="tight")

print(f"Total mass out: {np.sum(mass_out):.2e} M_sun")