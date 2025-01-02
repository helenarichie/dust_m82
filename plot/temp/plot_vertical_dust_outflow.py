import sys
sys.path.insert(0, "/Users/helenarichie/GitHub/my_scripts/")
from hconfig import *

density_conversion = 5.028e-34/(3.24e-22)**3 # g/cm^3 to M_sun/kpc^3

plt.rcParams.update({'font.family': 'Helvetica'})
fontsize = 20
plt.rcParams.update({'font.size': fontsize})

date = "2024-10-25"
fields = ["dust_0", "dust_1", "dust_2", "dust_3"]

if date == "2024-08-28":
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

##################################################################
pad = 10
linewidth = 5.5
color_hot, color_mixed, color_cool = "#d43a4f", "thistle", "mediumaquamarine"
styles = ["solid", "dotted", "dashed", "dashdot"]
##################################################################

# plot outflow rates
ymin = np.amin(rates_cool) - pad
ymax = np.amax(rates_hot) + pad
xmin = np.amin(time_output) - pad
xmax = np.amax(time_output) + pad

fig = plt.figure(figsize=(9.9, 7.75))

for i, field in enumerate(fields):
    # print(len(rates_mixed[i]))
    plt.plot(time_output/1e3, np.sum(rates_hot, axis=2)[i], linestyle=styles[i], linewidth=linewidth-1, c=color_hot)
    plt.plot(time_output/1e3, np.sum(rates_mixed, axis=2)[i], linestyle=styles[i], linewidth=linewidth-1, c=color_mixed)
    plt.plot(time_output/1e3, np.sum(rates_cool, axis=2)[i], linestyle=styles[i], linewidth=linewidth-1, c=color_cool)

plt.yscale("log")
plt.plot(0, 0, linestyle=styles[0], label=r"$a=1~\mu$m", c="k")
plt.plot(0, 0, linestyle=styles[1], label=r"$a=0.1~\mu$m", c="k")
plt.plot(0, 0, linestyle=styles[2], label=r"$a=0.01~\mu$m", c="k")
plt.plot(0, 0, linestyle=styles[3], label=r"$a=0.001~\mu$m", c="k")
plt.plot(0, 0, label=r"hot", c=color_hot)
plt.plot(0, 0, label=r"mixed", c=color_mixed)
plt.plot(0, 0, label=r"cool", c=color_cool)
plt.legend(fontsize=15)
# plt.xlim(xmin/1e3, xmax/1e3)
plt.tick_params(axis='both', which='both', direction='in', color='black', top=1, right=1, length=9, width=2, reset=True)
plt.xlabel("Time [Myr]", fontsize=fontsize+3)
plt.ylabel(r"Outflow rate $[M_\odot\,yr^{-1}]$", fontsize=fontsize+5)
plt.tight_layout()
plt.savefig(pngdir + f"rates_{name}_dust.png", dpi=300, bbox_inches="tight")

# plot total outflow masses
ymin = np.amin(mass_out_cool) - pad
ymax = np.amax(mass_out_hot) + pad
xmin = np.amin(time_output) - pad
xmax = np.amax(time_output) + pad

fig = plt.figure(figsize=(9.9, 7.75))
for i, field in enumerate(fields):
    plt.semilogy(time_output/1e3, mass_out_hot[i], linewidth=linewidth-1, linestyle=styles[i], c=color_hot, zorder=0)
    plt.semilogy(time_output/1e3, mass_out_mixed[i], linewidth=linewidth-1, linestyle=styles[i], c=color_mixed, zorder=0)
    plt.semilogy(time_output/1e3, mass_out_cool[i], linewidth=linewidth-1, linestyle=styles[i], c=color_cool, zorder=0)

plt.plot(0, 0, linestyle=styles[0], label=r"$a=1~\mu$m", c="k")
plt.plot(0, 0, linestyle=styles[1], label=r"$a=0.1~\mu$m", c="k")
plt.plot(0, 0, linestyle=styles[2], label=r"$a=0.01~\mu$m", c="k")
plt.plot(0, 0, linestyle=styles[3], label=r"$a=0.001~\mu$m", c="k")
plt.plot(0, 0, label=r"hot", c=color_hot)
plt.plot(0, 0, label=r"mixed", c=color_mixed)
plt.plot(0, 0, label=r"cool", c=color_cool)
plt.legend(fontsize=15)
# plt.xlim(xmin/1e3, xmax/1e3)
plt.tick_params(axis='both', which='both', direction='in', color='black', top=1, right=1, length=9, width=2, reset=True)
# plt.xticks(np.linspace(0, xmax/1e3, 5).round(1))
# plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
plt.xlabel("Time [Myr]", fontsize=fontsize+3)
plt.ylabel(r"$m_{out}$" + " " + r"$[M_\odot]$", fontsize=fontsize+5)
plt.tight_layout()
plt.savefig(pngdir + f"fluxes_{name}_dust.png", dpi=300, bbox_inches="tight")
plt.close()

fig = plt.figure(figsize=(9.9, 7.75))

plt.plot(0, 0, linestyle=styles[0], label=r"$a=1~\mu$m", c="k")
plt.plot(0, 0, linestyle=styles[1], label=r"$a=0.1~\mu$m", c="k")
plt.plot(0, 0, linestyle=styles[2], label=r"$a=0.01~\mu$m", c="k")
plt.plot(0, 0, linestyle=styles[3], label=r"$a=0.001~\mu$m", c="k")
plt.plot(0, 0, label=r"hot", c=color_hot)
plt.plot(0, 0, label=r"mixed", c=color_mixed)
plt.plot(0, 0, label=r"cool", c=color_cool)

print(f"Total hot-phase mass: {np.sum(mass_out_hot[0]):.1e}, {np.sum(mass_out_hot[1]):.1e}, {np.sum(mass_out_hot[2]):.1e}, {np.sum(mass_out_hot[3]):.1e} M_sun")
print(f"Total mixed-phase mass: {np.sum(mass_out_mixed[0]):.1e}, {np.sum(mass_out_mixed[1]):.1e}, {np.sum(mass_out_mixed[2]):.1e}, {np.sum(mass_out_mixed[3]):.1e} M_sun")
print(f"Total cool-phase mass: {np.sum(mass_out_cool[0]):.1e}, {np.sum(mass_out_cool[1]):.1e}, {np.sum(mass_out_cool[2]):.1e}, {np.sum(mass_out_cool[3]):.1e} M_sun")