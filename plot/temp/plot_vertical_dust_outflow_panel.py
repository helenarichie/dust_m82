import sys
sys.path.insert(0, "/Users/helenarichie/GitHub/my_scripts/")
from hconfig import *
import seaborn as sns

density_conversion = 5.028e-34/(3.24e-22)**3 # g/cm^3 to M_sun/kpc^3

plt.rcParams.update({'font.family': 'Helvetica'})
fontsize = 20
plt.rcParams.update({'font.size': fontsize})

date = "2024-11-01"
fields = ["dust_1", "dust_2", "dust_3"]

if (date == "2024-08-28") or (date == "2024-11-01"):
    name = "m82"
if (date == "2024-08-29") or (date == "2024-10-25"):
    name = "high-z"

##################################################################
basedir = f"/Users/helenarichie/Desktop/{date}/fluxes/"
pngdir = os.path.join(basedir, "png/")
csvdir = os.path.join(basedir, "csv/")
##################################################################

rates_hot = []
for field in fields:
    rate_i = []
    with open(os.path.join(csvdir, f"rate_{field}_hot_1e-24.csv")) as f:
        for line in f:
            line = line.split(",")
            rate_i.append(np.array(line, dtype=float))
    rates_hot.append(rate_i)

rates_mixed = []
for field in fields:
    rate_i = []
    with open(os.path.join(csvdir, f"rate_{field}_mixed_1e-24.csv")) as f:
        for line in f:
            line = line.split(",")
            rate_i.append(np.array(line, dtype=float))
    rates_mixed.append(rate_i)

rates_cool = []
for field in fields:
    rate_i = []
    with open(os.path.join(csvdir, f"rate_{field}_cool_1e-24.csv")) as f:
        for line in f:
            line = line.split(",")
            rate_i.append(np.array(line, dtype=float))
    rates_cool.append(rate_i)

time_output = []
with open(os.path.join(csvdir, "time_output_1e-24.csv")) as f:
    for line in f:
        time_output.append(float(line))
time_output = np.array(time_output)

dt_out = time_output[2] - time_output[1]

mass_out_hot = []
for rate in rates_hot:
    mass_out_i = []
    mass_cumulative = 0
    for i, rate_i in enumerate(rate):
        rate_i = np.sum(rate_i)
        mass_cumulative += rate_i * dt_out
        mass_out_i.append(mass_cumulative)
    mass_out_hot.append(mass_out_i)
mass_out_hot = np.array(mass_out_hot)

mass_out_mixed = []
for rate in rates_mixed:
    mass_out_i = []
    mass_cumulative = 0
    for i, rate_i in enumerate(rate):
        rate_i = np.sum(rate_i)
        mass_cumulative += rate_i * dt_out
        mass_out_i.append(mass_cumulative)
    mass_out_mixed.append(mass_out_i)
mass_out_mixed = np.array(mass_out_mixed)

mass_out_cool = []
for rate in rates_cool:
    mass_out_i = []
    mass_cumulative = 0
    for i, rate_i in enumerate(rate):
        rate_i = np.sum(rate_i)
        mass_cumulative += rate_i * dt_out
        mass_out_i.append(mass_cumulative)
    mass_out_cool.append(mass_out_i)
mass_out_cool = np.array(mass_out_cool)

# plot outflow rates
ymin = 1
ymax = 5e5
xmin = np.amin(time_output/1e3)
xmax = np.amax(time_output/1e3)

linewidth = 3
color_hot, color_mixed, color_cool = sns.color_palette(palette="flare", n_colors=3)
colors = [color_hot, color_mixed, color_cool]
styles = ["dashdot", "dotted", "dashed", "solid"]

fig, ax = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

for i, grain in enumerate(fields):
    ax[0].plot(time_output/1e3, mass_out_hot[i], linestyle=styles[i+1], linewidth=linewidth, c=color_hot)
ax[0].tick_params(axis='both', which="both", labelsize=15, top=True, right=True)
ax[0].set_yscale('log')
ax[0].set_ylabel(r"$m_{out}~[M_\odot]$", fontsize=20)
ax[0].set_xlabel(r"$t~[Myr]$", fontsize=20)
ax[0].set_xlim(xmin, xmax)
ax[0].set_ylim(ymin, ymax)
ax[0].vlines(30, ymin=ymin, ymax=ymax, linewidth=linewidth-0.5, zorder=0, color="lightgrey", alpha=0.7)

for i, grain in enumerate(fields):
    ax[1].plot(time_output/1e3, mass_out_mixed[i], linestyle=styles[i+1], linewidth=linewidth, c=color_mixed)
ax[1].tick_params(axis='both', which="both", labelsize=15, top=True, right=True)
ax[1].set_yscale('log')
ax[1].set_xlabel(r"$t~[Myr]$", fontsize=20)
ax[1].set_xlim(xmin, xmax)
ax[1].set_ylim(ymin, ymax)
ax[1].vlines(30, ymin=ymin, ymax=ymax, linewidth=linewidth-0.5, zorder=0, color="lightgrey", alpha=0.7)

for i, grain in enumerate(fields):
    ax[2].plot(time_output/1e3, mass_out_cool[i], linestyle=styles[i+1], linewidth=linewidth, c=color_cool)
ax[2].tick_params(axis='both', which="both", labelsize=15, top=True, right=True)
ax[2].set_yscale('log')
ax[2].set_xlabel(r"$t~[Myr]$", fontsize=20)
ax[2].set_xlim(xmin, xmax)
ax[2].set_ylim(ymin, ymax)
ax[2].vlines(30, ymin=ymin, ymax=ymax, linewidth=linewidth-0.5, zorder=0, color="lightgrey", alpha=0.7)
ax[2].plot(0, 0, linestyle=styles[1], label=r"$a=0.1~\mu$m", c="k", linewidth=linewidth)
ax[2].plot(0, 0, linestyle=styles[2], label=r"$a=0.01~\mu$m", c="k", linewidth=linewidth)
ax[2].plot(0, 0, linestyle=styles[3], label=r"$a=0.001~\mu$m", c="k", linewidth=linewidth)
ax[2].legend(fontsize=15, loc="upper left")

plt.tight_layout()
plt.savefig(pngdir + f"mass_out_dust.png", dpi=300)
plt.close()