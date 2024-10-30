import sys
sys.path.insert(0, "/ccs/home/helenarichie/code/my_scripts/")
from hconfig import *
from csv import writer

def calc_mass_loss_rate(rho, v, area):
    return np.sum(rho * np.abs(v) * area)

density_conversion = 5.028e-34/(3.24e-22)**3 # g/cm^3 to M_sun/kpc^3

################################################################
date = "2024-08-29"
rho_cl_i = 1e-24  # needed to index cloud material
cutoff = rho_cl_i*density_conversion/3 # M_sun/kpc^3
ns = 200
ne = 200
################################################################

basedir = f"/gpfs/alpine2/ast200/proj-shared/helena/{date}/"
datadir = os.path.join(basedir, "hdf5/edges/")
csvdir = os.path.join(basedir, "csv/")

cloud_csv_str = "rate_cloud_{:.0e}.csv".format(rho_cl_i)
dust_0_hot_csv_str = "rate_dust_0_hot_{:.0e}.csv".format(rho_cl_i)
dust_0_mixed_csv_str = "rate_dust_0_mixed_{:.0e}.csv".format(rho_cl_i)
dust_0_cool_csv_str = "rate_dust_0_cool_{:.0e}.csv".format(rho_cl_i)
dust_1_hot_csv_str = "rate_dust_1_hot_{:.0e}.csv".format(rho_cl_i)
dust_1_mixed_csv_str = "rate_dust_1_mixed_{:.0e}.csv".format(rho_cl_i)
dust_1_cool_csv_str = "rate_dust_1_cool_{:.0e}.csv".format(rho_cl_i)
dust_2_hot_csv_str = "rate_dust_2_hot_{:.0e}.csv".format(rho_cl_i)
dust_2_mixed_csv_str = "rate_dust_2_mixed_{:.0e}.csv".format(rho_cl_i)
dust_2_cool_csv_str = "rate_dust_2_cool_{:.0e}.csv".format(rho_cl_i)
dust_3_hot_csv_str = "rate_dust_3_hot_{:.0e}.csv".format(rho_cl_i)
dust_3_mixed_csv_str = "rate_dust_3_mixed_{:.0e}.csv".format(rho_cl_i)
dust_3_cool_csv_str = "rate_dust_3_cool_{:.0e}.csv".format(rho_cl_i)
time_csv_str = "time_output_{:.0e}.csv".format(rho_cl_i)

if ns == 0:
    f = open(os.path.join(csvdir, cloud_csv_str), "w")
    f.close()
    f = open(os.path.join(csvdir, dust_0_csv_str), "w")
    f.close()
    f = open(os.path.join(csvdir, dust_1_csv_str), "w")
    f.close()
    f = open(os.path.join(csvdir, dust_2_csv_str), "w")
    f.close()
    f = open(os.path.join(csvdir, dust_3_csv_str), "w")
    f.close()
    f = open(os.path.join(csvdir, time_csv_str), "w")
    f.close()

f = h5py.File(os.path.join(datadir, "0_edges.h5"))
head = f.attrs
nx, ny, nz = head["dims"]
dx, dy, dz = head["dx"]

files = glob.glob(os.path.join(datadir, "*.h5"))

ms = ["mz_minus_xy", "my_minus_xz", "mx_minus_yz", "mz_plus_xy", "my_plus_xz", "mx_plus_yz"]

# loop through hdf5 files to write out rates and masses for cloud and dust
for n in range(ns, ne+1):
    # read in data
    print(f"Starting file {n}.\n")
    fh5 = h5py.File(os.path.join(datadir, str(n)+"_edges.h5"))
    keys_gas_energy = ['GE_minus_xy', 'GE_minus_xz', 'GE_minus_yz', 'GE_plus_xy', 'GE_plus_xz', 'GE_plus_yz']
    keys_energy = ['E_minus_xy', 'E_minus_xz', 'E_minus_yz', 'E_plus_xy', 'E_plus_xz', 'E_plus_yz']
    keys_dust_0 = ['d_dust_0_minus_xy', 'd_dust_0_minus_xz', 'd_dust_0_minus_yz', 'd_dust_0_plus_xy', 'd_dust_0_plus_xz', 'd_dust_0_plus_yz']
    keys_dust_1 = ['d_dust_1_minus_xy', 'd_dust_1_minus_xz', 'd_dust_1_minus_yz', 'd_dust_1_plus_xy', 'd_dust_1_plus_xz', 'd_dust_1_plus_yz']
    keys_dust_2 = ['d_dust_2_minus_xy', 'd_dust_2_minus_xz', 'd_dust_2_minus_yz', 'd_dust_2_plus_xy', 'd_dust_2_plus_xz', 'd_dust_2_plus_yz']
    keys_dust_3 = ['d_dust_3_minus_xy', 'd_dust_3_minus_xz', 'd_dust_3_minus_yz', 'd_dust_3_plus_xy', 'd_dust_3_plus_xz', 'd_dust_3_plus_yz']
    keys_gas = ['d_minus_xy', 'd_minus_xz', 'd_minus_yz', 'd_plus_xy', 'd_plus_xz', 'd_plus_yz']
    keys_mx = ['mx_minus_xy', 'mx_minus_xz', 'mx_minus_yz', 'mx_plus_xy', 'mx_plus_xz', 'mx_plus_yz']
    keys_my = ['my_minus_xy', 'my_minus_xz', 'my_minus_yz', 'my_plus_xy', 'my_plus_xz', 'my_plus_yz']
    keys_mz = ['mz_minus_xy', 'mz_minus_xz', 'mz_minus_yz', 'mz_plus_xy', 'mz_plus_xz', 'mz_plus_yz']
    keys_scalar = ['basic_scalar_minus_xy', 'basic_scalar_minus_xz', 'basic_scalar_minus_yz', 'basic_scalar_plus_xy', 'basic_scalar_plus_xz', 'basic_scalar_plus_yz']

    head = fh5.attrs
    nx, ny, nz = head["dims"]
    dx, dy, dz = head["dx"]
    t = head["t"]
    density_unit = head["density_unit"]
    energy_unit = head["energy_unit"]
    velocity_unit = head["velocity_unit"]
    pressure_unit = density_unit * velocity_unit ** 2
    gamma = head["gamma"]
    MP = 1.672622e-24 # proton mass, g
    KB = 1.380658e-16 # Boltzmann constant, cm^2 g s^-2 K^-1

    rates_cloud = []
    rates_dust_0_hot, rates_dust_0_mixed, rates_dust_0_cool = [], [], []
    rates_dust_1_hot, rates_dust_1_mixed, rates_dust_1_cool = [], [], []
    rates_dust_2_hot, rates_dust_2_mixed, rates_dust_2_cool = [], [], []
    rates_dust_3_hot, rates_dust_3_mixed, rates_dust_3_cool = [], [], []

    for i, key in enumerate(keys_gas):
        velocity, mask = None, None

        gas = fh5[keys_gas[i]][()]
        dust_0 = fh5[keys_dust_0[i]][()]
        dust_1 = fh5[keys_dust_1[i]][()]
        dust_2 = fh5[keys_dust_2[i]][()]
        dust_3 = fh5[keys_dust_3[i]][()]

        def calc_temp(gamma, mu, mp, kb, density, energy, momentum_x, momentum_y, momentum_z, energy_unit, velocity_unit, density_unit):
            n = (density * density_unit) / (mu * mp)
            v_squared = ((momentum_x / density) * velocity_unit) ** 2 + ((momentum_y / density) * velocity_unit) ** 2 + ((momentum_z / density) * velocity_unit) ** 2
            return ((gamma - 1) / (n * kb)) * ((energy * energy_unit) - (0.5 * density * density_unit * v_squared))
        

        def calc_temp_DE(gamma, mu, mp, kb, density, gas_energy, density_unit, pressure_unit):
            n = density * density_unit / (mu * mp)
            return gas_energy * (gamma - 1) * pressure_unit / (n * kb)
        
        temp = calc_temp(gamma, 0.6, MP, KB, gas, fh5[keys_energy[i]][()], fh5[keys_mx[i]][()], fh5[keys_my[i]][()], fh5[keys_mz[i]][()], energy_unit, velocity_unit, density_unit)
        # temp = calc_temp_DE(gamma, 0.6, MP, KB, gas, fh5[keys_energy[i]][()], density_unit, pressure_unit

        if i <= 2:
            velocity = fh5[ms[i]] / gas
            mask = np.logical_and(gas >= cutoff, velocity < 0)
        if i > 2:
            velocity = fh5[ms[i]] / gas
            mask = np.logical_and(gas >= cutoff, velocity > 0)

        rates_cloud.append(calc_mass_loss_rate(gas[mask], velocity[mask], dx**2))

        if i <= 2:
            velocity = fh5[ms[i]] / gas
            mask_hot = np.logical_and(np.logical_and(temp >= 5e5, dust_0 >= 0), velocity < 0)
            mask_mixed = np.logical_and(np.logical_and(np.logical_and(temp <= 2e4, temp < 5e5), dust_0 >= 0), velocity < 0)
            mask_cool = np.logical_and(np.logical_and(temp < 2e4, dust_0 >= 0), velocity < 0)
        if i > 2:
            velocity = fh5[ms[i]] / gas
            mask_hot = np.logical_and(np.logical_and(temp >= 5e5, dust_0 >= 0), velocity > 0)
            mask_mixed = np.logical_and(np.logical_and(np.logical_and(temp <= 2e4, temp < 5e5), dust_0 >= 0), velocity > 0)
            mask_cool = np.logical_and(np.logical_and(temp < 2e4, dust_0 >= 0), velocity > 0)
        
        rates_dust_0_hot.append(calc_mass_loss_rate(dust_0[mask_hot], velocity[mask_hot], dx**2))
        rates_dust_0_mixed.append(calc_mass_loss_rate(dust_0[mask_mixed], velocity[mask_mixed], dx**2))
        rates_dust_0_cool.append(calc_mass_loss_rate(dust_0[mask_cool], velocity[mask_cool], dx**2))

        if i <= 2:
            velocity = fh5[ms[i]] / gas
            mask_hot = np.logical_and(np.logical_and(temp >= 5e5, dust_1 >= 0), velocity < 0)
            mask_mixed = np.logical_and(np.logical_and(np.logical_and(temp <= 2e4, temp < 5e5), dust_1 >= 0), velocity < 0)
            mask_cool = np.logical_and(np.logical_and(temp < 2e4, dust_1 >= 0), velocity < 0)
        if i > 2:
            velocity = fh5[ms[i]] / gas
            mask_hot = np.logical_and(np.logical_and(temp >= 5e5, dust_1 >= 0), velocity > 0)
            mask_mixed = np.logical_and(np.logical_and(np.logical_and(temp <= 2e4, temp < 5e5), dust_1 >= 0), velocity > 0)
            mask_cool = np.logical_and(np.logical_and(temp < 2e4, dust_1 >= 0), velocity > 0)

        rates_dust_1_hot.append(calc_mass_loss_rate(dust_1[mask_hot], velocity[mask_hot], dx**2))
        rates_dust_1_mixed.append(calc_mass_loss_rate(dust_1[mask_mixed], velocity[mask_mixed], dx**2))
        rates_dust_1_cool.append(calc_mass_loss_rate(dust_1[mask_cool], velocity[mask_cool], dx**2))

        if i <= 2:
            velocity = fh5[ms[i]] / gas
            mask_hot = np.logical_and(np.logical_and(temp >= 5e5, dust_2 >= 0), velocity < 0)
            mask_mixed = np.logical_and(np.logical_and(np.logical_and(temp <= 2e4, temp < 5e5), dust_2 >= 0), velocity < 0)
            mask_cool = np.logical_and(np.logical_and(temp < 2e4, dust_2 >= 0), velocity < 0)
        if i > 2:
            velocity = fh5[ms[i]] / gas
            mask_hot = np.logical_and(np.logical_and(temp >= 5e5, dust_2 >= 0), velocity > 0)
            mask_mixed = np.logical_and(np.logical_and(np.logical_and(temp <= 2e4, temp < 5e5), dust_2 >= 0), velocity > 0)
            mask_cool = np.logical_and(np.logical_and(temp < 2e4, dust_2 >= 0), velocity > 0)

        rates_dust_2_hot.append(calc_mass_loss_rate(dust_2[mask_hot], velocity[mask_hot], dx**2))
        rates_dust_2_mixed.append(calc_mass_loss_rate(dust_2[mask_mixed], velocity[mask_mixed], dx**2))
        rates_dust_2_cool.append(calc_mass_loss_rate(dust_2[mask_cool], velocity[mask_cool], dx**2))

        if i <= 2:
            velocity = fh5[ms[i]] / gas
            mask_hot = np.logical_and(np.logical_and(temp >= 5e5, dust_3 >= 0), velocity < 0)
            mask_mixed = np.logical_and(np.logical_and(np.logical_and(temp <= 2e4, temp < 5e5), dust_3 >= 0), velocity < 0)
            mask_cool = np.logical_and(np.logical_and(temp < 2e4, dust_3 >= 0), velocity < 0)
        if i > 2:
            velocity = fh5[ms[i]] / gas
            mask_hot = np.logical_and(np.logical_and(temp >= 5e5, dust_3 >= 0), velocity > 0)
            mask_mixed = np.logical_and(np.logical_and(np.logical_and(temp <= 2e4, temp < 5e5), dust_3 >= 0), velocity > 0)
            mask_cool = np.logical_and(np.logical_and(temp < 2e4, dust_3 >= 0), velocity > 0)

        rates_dust_3_hot.append(calc_mass_loss_rate(dust_2[mask_hot], velocity[mask_hot], dx**2))
        rates_dust_3_mixed.append(calc_mass_loss_rate(dust_2[mask_mixed], velocity[mask_mixed], dx**2))
        rates_dust_3_cool.append(calc_mass_loss_rate(dust_2[mask_cool], velocity[mask_cool], dx**2))

    with open(os.path.join(csvdir, cloud_csv_str), "a") as f:
        writer_obj = writer(f)
        writer_obj.writerow(rates_cloud)
        f.close()

    with open(os.path.join(csvdir, dust_0_hot_csv_str), "a") as f:
        writer_obj = writer(f)
        writer_obj.writerow(rates_dust_0_hot)
        f.close()

    with open(os.path.join(csvdir, dust_0_mixed_csv_str), "a") as f:
        writer_obj = writer(f)
        writer_obj.writerow(rates_dust_0_mixed)
        f.close()

    with open(os.path.join(csvdir, dust_0_cool_csv_str), "a") as f:
        writer_obj = writer(f)
        writer_obj.writerow(rates_dust_0_cool)
        f.close()

    with open(os.path.join(csvdir, dust_1_hot_csv_str), "a") as f:
        writer_obj = writer(f)
        writer_obj.writerow(rates_dust_1_hot)
        f.close()

    with open(os.path.join(csvdir, dust_1_mixed_csv_str), "a") as f:
        writer_obj = writer(f)
        writer_obj.writerow(rates_dust_1_mixed)
        f.close()

    with open(os.path.join(csvdir, dust_1_cool_csv_str), "a") as f:
        writer_obj = writer(f)
        writer_obj.writerow(rates_dust_1_cool)
        f.close()

    with open(os.path.join(csvdir, dust_2_hot_csv_str), "a") as f:
        writer_obj = writer(f)
        writer_obj.writerow(rates_dust_2_hot)
        f.close()

    with open(os.path.join(csvdir, dust_2_mixed_csv_str), "a") as f:
        writer_obj = writer(f)
        writer_obj.writerow(rates_dust_2_mixed)
        f.close()

    with open(os.path.join(csvdir, dust_2_cool_csv_str), "a") as f:
        writer_obj = writer(f)
        writer_obj.writerow(rates_dust_2_cool)
        f.close()

    with open(os.path.join(csvdir, dust_3_hot_csv_str), "a") as f:
        writer_obj = writer(f)
        writer_obj.writerow(rates_dust_3_hot)
        f.close()

    with open(os.path.join(csvdir, dust_3_mixed_csv_str), "a") as f:
        writer_obj = writer(f)
        writer_obj.writerow(rates_dust_3_mixed)
        f.close()

    with open(os.path.join(csvdir, dust_3_cool_csv_str), "a") as f:
        writer_obj = writer(f)
        writer_obj.writerow(rates_dust_3_cool)
        f.close()

    with open(os.path.join(csvdir, time_csv_str), "a") as f:
        writer_obj = writer(f)
        writer_obj.writerow(t)
        f.close()
