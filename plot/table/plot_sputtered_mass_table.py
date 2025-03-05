import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import os
import sys
import pathlib
import seaborn as sns
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent.resolve(), "../utils/"))
from read_cmdline import read_cmdline
from read_vertical_profiles import read_vertical_profiles

def main(basedir, field_names, time, exclude_disk, simulation, weight, tail):

    sputtered_names = ["sputtered_0", "sputtered_1", "sputtered_2", "sputtered_3"]
    gas_name = ["gas"]

    vertical_dir = os.path.join(basedir, "profiles/vertical/csv/")
        
    times, mass_hot, mass_mixed, mass_cool = read_vertical_profiles(vertical_dir, field_names)
    _, sputtered_hot, sputtered_mixed, sputtered_cool = read_vertical_profiles(vertical_dir, sputtered_names[0:len(field_names)])
    _, gas_hot, gas_mixed, gas_cool = read_vertical_profiles(vertical_dir, gas_name)

    gas_hot, gas_mixed, gas_cool = gas_hot[0], gas_mixed[0], gas_cool[0]

    fnum = int(time * 2 / 100)

    wh_time = np.where(times==time)[0][0]

    table_data_sput = np.zeros((2, 3*len(field_names)))
    table_data_mass = np.zeros((2, 3*len(field_names)))
    table_data_gas = np.zeros((2, 3))

    initial_mass = None

    plt.rcParams.update({'font.size': 10})

    for n, name in enumerate(field_names):

        initial_mass = np.sum(sputtered_cool[n][0][:])+np.sum(sputtered_mixed[n][0][:])+np.sum(sputtered_hot[n][0][:])+np.sum(mass_cool[n][0][:])+np.sum(mass_mixed[n][0][:])+np.sum(mass_hot[n][0][:])

        sputtered_hot_outflow, sputtered_mixed_outflow, sputtered_cool_outflow = np.sum(sputtered_hot[n][wh_time][1:]), np.sum(sputtered_mixed[n][wh_time][1:]), np.sum(sputtered_cool[n][wh_time][1:])
        mass_hot_outflow, mass_mixed_outflow, mass_cool_outflow = np.sum(mass_hot[n][wh_time][1:]), np.sum(mass_mixed[n][wh_time][1:]), np.sum(mass_cool[n][wh_time][1:])
        gas_hot_outflow, gas_mixed_outflow, gas_cool_outflow = np.sum(gas_hot[wh_time][1:]), np.sum(gas_mixed[wh_time][1:]), np.sum(gas_cool[wh_time][1:])

        table_data_sput[0][n+0] = sputtered_hot_outflow
        table_data_sput[0][n+3] = sputtered_mixed_outflow
        table_data_sput[0][n+6] = sputtered_cool_outflow

        table_data_mass[0][n+0] = mass_hot_outflow
        table_data_mass[0][n+3] = mass_mixed_outflow
        table_data_mass[0][n+6] = mass_cool_outflow

        table_data_gas[0][0] = gas_hot_outflow
        table_data_gas[0][1] = gas_mixed_outflow
        table_data_gas[0][2] = gas_cool_outflow

    vertical_dir = os.path.join(basedir, "/Users/helenarichie/Desktop/2024-10-25/profiles/vertical/csv/")
    times, mass_hot, mass_mixed, mass_cool = read_vertical_profiles(vertical_dir, field_names)
    _, sputtered_hot, sputtered_mixed, sputtered_cool = read_vertical_profiles(vertical_dir, sputtered_names[0:len(field_names)])
    _, gas_hot, gas_mixed, gas_cool = read_vertical_profiles(vertical_dir, gas_name)

    gas_hot, gas_mixed, gas_cool = gas_hot[0], gas_mixed[0], gas_cool[0]

    for n, name in enumerate(field_names):

        initial_mass = np.sum(sputtered_cool[n][0][:])+np.sum(sputtered_mixed[n][0][:])+np.sum(sputtered_hot[n][0][:])+np.sum(mass_cool[n][0][:])+np.sum(mass_mixed[n][0][:])+np.sum(mass_hot[n][0][:])
        sputtered_hot_outflow, sputtered_mixed_outflow, sputtered_cool_outflow = np.sum(sputtered_hot[n][wh_time][1:]), np.sum(sputtered_mixed[n][wh_time][1:]), np.sum(sputtered_cool[n][wh_time][1:])
        mass_hot_outflow, mass_mixed_outflow, mass_cool_outflow = np.sum(mass_hot[n][wh_time][1:]), np.sum(mass_mixed[n][wh_time][1:]), np.sum(mass_cool[n][wh_time][1:])
        gas_hot_outflow, gas_mixed_outflow, gas_cool_outflow = np.sum(gas_hot[wh_time][1:]), np.sum(gas_mixed[wh_time][1:]), np.sum(gas_cool[wh_time][1:])

        table_data_sput[1][n+0] = sputtered_hot_outflow
        table_data_sput[1][n+3] = sputtered_mixed_outflow
        table_data_sput[1][n+6] = sputtered_cool_outflow

        table_data_mass[1][n+0] = mass_hot_outflow
        table_data_mass[1][n+3] = mass_mixed_outflow
        table_data_mass[1][n+6] = mass_cool_outflow

        table_data_gas[1][0] = gas_hot_outflow
        table_data_gas[1][1] = gas_mixed_outflow
        table_data_gas[1][2] = gas_cool_outflow

    fig, ax = plt.subplots(figsize=(10,4))
    cmap = sns.color_palette("light:steelblue", as_cmap=True)

    label_0, label_1, label_2 = r"$1~\mu$m", r"$0.1~\mu$m", r"$0.01~\mu$m"
    rowlabels = ["m82", "high-z"]
    ax.axis('off')
    collabels = [label_0, label_1, label_2, label_0, label_1, label_2, label_0, label_1, label_2]
    norm = colors.LogNorm(vmin=table_data_sput.min(), vmax=table_data_sput.max())
    color_hot, color_mixed, color_cool = sns.color_palette(palette="flare", n_colors=3)

    header = plt.table(cellText=[[r'$m_{sp,hot}\,\,\,[M_\odot]$', r"$m_{sp,mixed}\,\,\,[M_\odot]$", r"$m_{sp,cool}\,\,\,[M_\odot]$"]], loc="center", cellLoc="center", cellColours=[[color_hot, color_mixed, color_cool]], alpha=0.3, fontsize=10)
    header.scale(1, 1.7)

    for k, cell in header._cells.items():
        cell.set_alpha(0.7)

    table = ax.table(cellText=np.round(table_data_sput, 2),
                            cellColours=cmap(norm(table_data_sput)), colLabels=collabels, rowLabels=rowlabels, loc="bottom",
                             bbox=[0, 0.175, 1.0, 0.3], cellLoc="center", fontsize=10)

    for i in range(table_data_sput.shape[0]):
        for j in range(table_data_sput.shape[1]):
            cell = table[i + 1, j]  # i+1 to skip header row
            cell.set_text_props(ha='center')
            cell.get_text().set_text(f'{table_data_sput[i, j]:.2e}')

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    plt.tight_layout()
    plt.savefig("/Users/helenarichie/Desktop/table_sput.png", dpi=300, bbox_inches="tight")

    fig, ax = plt.subplots(figsize=(10,4))
    cmap = sns.color_palette("light:steelblue", as_cmap=True)

    label_0, label_1, label_2 = r"$1~\mu$m", r"$0.1~\mu$m", r"$0.01~\mu$m"
    rowlabels = ["m82", "high-z"]
    ax.axis('off')
    collabels = [label_0, label_1, label_2, label_0, label_1, label_2, label_0, label_1, label_2]
    norm = colors.LogNorm(vmin=table_data_mass.min(), vmax=table_data_mass.max())
    color_hot, color_mixed, color_cool = sns.color_palette(palette="flare", n_colors=3)

    header = plt.table(cellText=[[r'$m_{dust,hot}\,\,\,[M_\odot]$', r"$m_{dust,mixed}\,\,\,[M_\odot]$", r"$m_{dust,cool}\,\,\,[M_\odot]$"]], loc="center", cellLoc="center", cellColours=[[color_hot, color_mixed, color_cool]], alpha=0.3)
    header.scale(1, 1.7)

    for k, cell in header._cells.items():
        cell.set_alpha(0.7)

    table = ax.table(cellText=np.round(table_data_mass, 2),
                            cellColours=cmap(norm(table_data_mass)), colLabels=collabels, rowLabels=rowlabels, loc="bottom",
                             bbox=[0, 0.175, 1.0, 0.3], cellLoc="center", fontsize=10)

    for i in range(table_data_mass.shape[0]):
        for j in range(table_data_mass.shape[1]):
            cell = table[i + 1, j]  # i+1 to skip header row
            cell.set_text_props(ha='center')
            cell.get_text().set_text(f'{table_data_mass[i, j]:.2e}')

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    plt.tight_layout()
    plt.savefig("/Users/helenarichie/Desktop/table_mass.png", dpi=300)

    fig, ax = plt.subplots(figsize=(10,4))

    rowlabels = ["m82", "high-z"]
    ax.axis('off')
    collabels = [r'$m_{gas,hot}\,\,\,[M_\odot]$', r"$m_{gas,mixed}\,\,\,[M_\odot]$", r"$m_{gas,cool}\,\,\,[M_\odot]$"]
    color_hot, color_mixed, color_cool = sns.color_palette(palette="flare", n_colors=3)

    # header = plt.table(cellText=[[r'$m_{tot,hot}\,\,\,[M_\odot]$', r"$m_{tot,mixed}\,\,\,[M_\odot]$", r"$m_{tot,cool}\,\,\,[M_\odot]$"]], loc="center", cellLoc="center", cellColours=[[color_hot, color_mixed, color_cool]], alpha=0.3)
    # header.scale(1, 1.7)

    # for k, cell in header._cells.items():
    #     cell.set_alpha(0.7)

    table = ax.table(cellText=np.round(table_data_gas, 2),
                            cellColours=cmap(norm(table_data_gas)), colLabels=collabels, rowLabels=rowlabels, loc="bottom",
                             bbox=[0, 0.175, 1.0, 0.3], cellLoc="center", fontsize=10)

    for i in range(table_data_gas.shape[0]):
        for j in range(table_data_gas.shape[1]):
            cell = table[i + 1, j]  # i+1 to skip header row
            cell.set_text_props(ha='center')
            cell.get_text().set_text(f'{table_data_gas[i, j]:.2e}')

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    plt.tight_layout()
    plt.savefig("/Users/helenarichie/Desktop/table_gas.png", dpi=300)

if __name__ == "__main__":
    args = read_cmdline()

    sys.path.insert(0, args.configdir)
    import hconfig

    basedir = args.basedir
    field_names = args.field_names
    time = args.sim_time
    exclude_disk = args.exclude_disk
    weight = args.weight
    tail = args.tail
    simulation = args.simulation


    main(basedir, field_names, time, exclude_disk, simulation, weight, tail)