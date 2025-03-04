import numpy as np
import os
import sys
import pathlib
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent.resolve(), "../utils/"))
from read_cmdline import read_cmdline
from read_radial_profile import read_radial_profile
from read_vertical_profiles import read_vertical_profiles

def main(basedir, field_names, time, exclude_disk, simulation, weight, tail):

    sputtered_names = ["sputtered_0", "sputtered_1", "sputtered_2", "sputtered_3"]

    vertical_dir = os.path.join(basedir, "profiles/vertical/csv/")
    radial_dir = os.path.join(basedir, "profiles/radial/")
        
    times, mass_hot, mass_mixed, mass_cool = read_vertical_profiles(vertical_dir, field_names)
    _, sputtered_hot, sputtered_mixed, sputtered_cool = read_vertical_profiles(vertical_dir, sputtered_names[0:len(field_names)])

    fnum = int(time * 2 / 100)

    bin_tot, gas_hot, dust_hot, _, _, _, _, _, _, _ = read_radial_profile(radial_dir, fnum, simulation, "hot", weight, tail)
    _, gas_cool, dust_cool, _, _, _, _, _, _, _ = read_radial_profile(radial_dir ,fnum, simulation, "cold", weight, tail)

    wh_time = np.where(times==time)[0][0]

    # print(dust_cool[0]-dust_cool[2])

    # print(dust_cool[2]/mass_cool[2][wh_time][0])
    # print(mass_cool[0][wh_time]-mass_cool[2][wh_time])
    # print(sputtered_cool[2][wh_time])

    # print(f"Total cool gas mass: {np.sum(gas_cool):.4e}")
    # print(f"Total hot gas mass: {np.sum(gas_hot):.4e}")
    
    table_data = np.zeros((len(field_names), 3))

    for n, name in enumerate(field_names):

        initial_mass = np.sum(sputtered_cool[n][0][:])+np.sum(sputtered_mixed[n][0][:])+np.sum(sputtered_hot[n][0][:])+np.sum(mass_cool[n][0][:])+np.sum(mass_mixed[n][0][:])+np.sum(mass_hot[n][0][:])

        print(f"\n########################### {time/1e3} Myr, {name}, {simulation} ###############################")
        hot_dgr = dust_hot[n] / gas_hot
        cool_dgr = dust_cool[n] / gas_cool

        sputtered_hot_time, sputtered_mixed_time, sputtered_cool_time = np.sum(sputtered_hot[n][wh_time][:]), np.sum(sputtered_mixed[n][wh_time][:]), np.sum(sputtered_cool[n][wh_time][:])
        mass_hot_time, mass_mixed_time, mass_cool_time = np.sum(mass_hot[n][wh_time][:]), np.sum(mass_mixed[n][wh_time][:]), np.sum(mass_cool[n][wh_time][:])
        total_sputtered_time = sputtered_hot_time + sputtered_mixed_time + sputtered_cool_time
        total_mass_time = mass_hot_time + mass_mixed_time + mass_cool_time

        sputtered_hot_outflow, sputtered_mixed_outflow, sputtered_cool_outflow = np.sum(sputtered_hot[n][wh_time][1:]), np.sum(sputtered_mixed[n][wh_time][1:]), np.sum(sputtered_cool[n][wh_time][1:])

        if exclude_disk:
            sputtered_hot_disk, sputtered_mixed_disk, sputtered_cool_disk = np.sum(sputtered_hot[n][wh_time][0]), np.sum(sputtered_mixed[n][wh_time][0]), np.sum(sputtered_cool[n][wh_time][0])
            total_hot_disk, total_mixed_disk, total_cool_disk = np.sum(mass_hot[n][wh_time][0]), np.sum(mass_mixed[n][wh_time][0]), np.sum(mass_cool[n][wh_time][0])
            # print(f"\nHot {name} sputtered in disk: {sputtered_hot_disk/initial_mass:.3e}")
            # print(f"Mixed {name} sputtered in disk: {sputtered_mixed_disk/initial_mass:.3e}")
            # print(f"Cool {name} sputtered in disk: {sputtered_cool_disk/initial_mass:.3e}")
            # print(f"Total {name} sputtered in disk: {(sputtered_hot_disk+sputtered_mixed_disk+sputtered_cool_disk)/initial_mass:.3e}")
            total_sputtered_e = sputtered_hot_disk + sputtered_mixed_disk + sputtered_cool_disk
            total_mass_e = total_hot_disk + total_mixed_disk + total_cool_disk
            print(f"exclude_disk {name} outflow mass: {initial_mass-(total_sputtered_e+total_mass_e):.3e}")

        print(f"{name} outflow mass mass: {(initial_mass-(total_sputtered_time+total_mass_time)):.3e} M_sun")

if __name__ == "__main__":
    args = read_cmdline()

    basedir = args.basedir
    field_names = args.field_names
    time = args.time
    exclude_disk = args.exclude_disk
    weight = args.weight
    tail = args.tail
    simulation = args.simulation


    main(basedir, field_names, time, exclude_disk, simulation, weight, tail)