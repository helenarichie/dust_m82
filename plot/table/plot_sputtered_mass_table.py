import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import os
import sys
import pathlib
import seaborn as sns
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent.resolve(), "../..//utils/"))
from read_cmdline import read_cmdline
from read_vertical_profiles import read_vertical_profiles

def main(basedir, field_names, time, exclude_disk, simulation, weight, tail):

    sputtered_names = ["sputtered_0", "sputtered_1", "sputtered_2", "sputtered_3"]
    vertical_dir = os.path.join(basedir, "profiles/vertical/csv/short/")
        
    times, mass_hot, mass_mixed, mass_cool = read_vertical_profiles(vertical_dir, field_names)
    _, sputtered_hot, sputtered_mixed, sputtered_cool = read_vertical_profiles(vertical_dir, sputtered_names[0:len(field_names)])

    wh_time = np.where(times==time)[0][0]

    table_data = np.zeros((6, 3*len(field_names)))

    for n, name in enumerate(field_names):

        sputtered_hot_outflow, sputtered_mixed_outflow, sputtered_cool_outflow = np.sum(sputtered_hot[n][wh_time][1:]), np.sum(sputtered_mixed[n][wh_time][1:]), np.sum(sputtered_cool[n][wh_time][1:])
        mass_hot_outflow, mass_mixed_outflow, mass_cool_outflow = np.sum(mass_hot[n][wh_time][1:]), np.sum(mass_mixed[n][wh_time][1:]), np.sum(mass_cool[n][wh_time][1:])

        table_data[0][n+0] = mass_hot_outflow
        table_data[0][n+3] = mass_mixed_outflow
        table_data[0][n+6] = mass_cool_outflow
        
        table_data[1][n+0] = sputtered_hot_outflow
        table_data[1][n+3] = sputtered_mixed_outflow
        table_data[1][n+6] = sputtered_cool_outflow

        table_data[2][n+0] = sputtered_hot_outflow/mass_hot_outflow
        table_data[2][n+3] = sputtered_mixed_outflow/mass_mixed_outflow
        table_data[2][n+6] = sputtered_cool_outflow/mass_cool_outflow

    vertical_dir = os.path.join(basedir, "/Users/helenarichie/Desktop/2024-10-25/profiles/vertical/csv/short/")
    times, mass_hot, mass_mixed, mass_cool = read_vertical_profiles(vertical_dir, field_names)
    _, sputtered_hot, sputtered_mixed, sputtered_cool = read_vertical_profiles(vertical_dir, sputtered_names[0:len(field_names)])

    for n, name in enumerate(field_names):

        sputtered_hot_outflow, sputtered_mixed_outflow, sputtered_cool_outflow = np.sum(sputtered_hot[n][wh_time][1:]), np.sum(sputtered_mixed[n][wh_time][1:]), np.sum(sputtered_cool[n][wh_time][1:])
        mass_hot_outflow, mass_mixed_outflow, mass_cool_outflow = np.sum(mass_hot[n][wh_time][1:]), np.sum(mass_mixed[n][wh_time][1:]), np.sum(mass_cool[n][wh_time][1:])

        table_data[3][n+0] = mass_hot_outflow
        table_data[3][n+3] = mass_mixed_outflow
        table_data[3][n+6] = mass_cool_outflow

        table_data[4][n+0] = sputtered_hot_outflow
        table_data[4][n+3] = sputtered_mixed_outflow
        table_data[4][n+6] = sputtered_cool_outflow

        table_data[5][n+0] = sputtered_hot_outflow/mass_hot_outflow
        table_data[5][n+3] = sputtered_mixed_outflow/mass_mixed_outflow
        table_data[5][n+6] = sputtered_cool_outflow/mass_cool_outflow

    fig, ax = plt.subplots(figsize=(10,8))
    plt.rcParams.update({'font.size': 10})

    cmap_dust_mass = sns.color_palette("light:plum", as_cmap=True)
    cmap_sput_mass = sns.color_palette("light:lightslategray", as_cmap=True)
    cmap_sput_norm = sns.color_palette("light:steelblue", as_cmap=True)

    # compute normalizations
    table_sub_dust_mass = np.concatenate((table_data[0], table_data[3]))  # only the dust mass data
    table_sub_sput_mass = np.concatenate((table_data[1], table_data[4]))  # only the sputtered mass data
    table_sub_sput_norm = np.concatenate((table_data[2], table_data[5]))  # only the normalized sputtered mass data
    norm_dust_mass = colors.LogNorm(vmin=table_sub_dust_mass.min(), vmax=table_sub_dust_mass.max())
    norm_sput_mass = colors.LogNorm(vmin=table_sub_sput_mass.min(), vmax=table_sub_sput_mass.max())
    norm_sput_norm = colors.LogNorm(vmin=table_sub_sput_norm.min(), vmax=table_sub_sput_norm.max()) 

    label_0, label_1, label_2 = r"$1~\mu$m", r"$0.1~\mu$m", r"$0.01~\mu$m"
    rowlabels = [r"$m_{dust}~[M_\odot]$", r"$m_{sp}~[M_\odot]$", r"$m_{sp}/m_{dust}$", r"$m_{dust}~[M_\odot]$", r"$m_{sp}~[M_\odot]$", r"$m_{sp}/m_{dust}$"]
    ax.axis('off')
    col_labels = [label_0, label_1, label_2, label_0, label_1, label_2, label_0, label_1, label_2]
    color_hot, color_mixed, color_cool = sns.color_palette(palette="flare", n_colors=3)

    header = plt.table(cellText=[[r"hot", r"mixed", r"cool"]], loc="center", cellLoc="center", cellColours=[[color_hot, color_mixed, color_cool]], alpha=0.3, fontsize=10)
    header.scale(1, 1.7)

    for k, cell in header._cells.items():
        cell.set_alpha(0.7)
        cell.get_text().set_weight("bold")

    table = ax.table(cellText=np.round(table_data, 1), colLabels=col_labels, rowLabels=rowlabels, loc="bottom", bbox=[0, 0.175, 1.0, 0.3], cellLoc="center", fontsize=10)

    for i, cell in enumerate(table._cells):
        if i < len(col_labels):
            table._cells[cell].get_text().set_weight('bold')

    for i, cell in enumerate(table.get_celld()):
        # if (cell[0] == 1 or cell[0] == 4) and cell[1] != -1:
        #     table[cell].set_facecolor(cmap_dust_mass(norm_dust_mass(table_data[cell[0]-1, cell[1]])))
        # if (cell[0] == 2 or cell[0] == 5) and cell[1] != -1:
        #     table[cell].set_facecolor(cmap_sput_mass(norm_sput_mass(table_data[cell[0]-1, cell[1]])))
        if (cell[0] == 3 or cell[0] == 6) and cell[1] != -1:
            table[cell].set_facecolor(cmap_sput_norm(norm_sput_norm(table_data[cell[0]-1, cell[1]])))

    for i in range(table_data.shape[0]):
        for j in range(table_data.shape[1]):
            cell = table[i + 1, j]  # i+1 to skip header row
            cell.set_text_props(ha='center')
            cell.get_text().set_text(f'{table_data[i, j]:.1e}')

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    plt.tight_layout()
    plt.savefig("/Users/helenarichie/Desktop/table_sput.pdf", dpi=300, bbox_inches="tight")

if __name__ == "__main__":
    args = read_cmdline()

    sys.path.insert(0, args.configdir)
    import hconfig

    basedir = args.basedir
    field_names = args.field_names
    time = args.time
    exclude_disk = args.exclude_disk
    weight = args.weight
    tail = args.tail
    simulation = args.simulation


    main(basedir, field_names, time, exclude_disk, simulation, weight, tail)