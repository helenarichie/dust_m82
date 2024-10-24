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
ns = 0
ne = 1000
################################################################

basedir = f"/gpfs/alpine2/ast200/proj-shared/helena/{date}/"
datadir = os.path.join(basedir, "hdf5/edges/")
csvdir = os.path.join(basedir, "csv/")

cloud_csv_str = "rate_cloud_{:.0e}.csv".format(rho_cl_i)
dust_0_csv_str = "rate_dust_0_{:.0e}.csv".format(rho_cl_i)
dust_1_csv_str = "rate_dust_1_{:.0e}.csv".format(rho_cl_i)
dust_2_csv_str = "rate_dust_2_{:.0e}.csv".format(rho_cl_i)
dust_3_csv_str = "rate_dust_3_{:.0e}.csv".format(rho_cl_i)
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

n_faces = 6
ns_gas = 8
ns_dust_0 = 4
ns_dust_1 = 5
ns_dust_2 = 6
ns_dust_3 = 7

ms = ["mz_minus_xy", "my_minus_xz", "mx_minus_yz", "mz_plus_xy", "my_plus_xz", "mx_plus_yz"]

# loop through hdf5 files to write out rates and masses for cloud and dust
for n in range(ns, len(files)):
    # read in data
    print(f"Starting file {n}.\n")
    fh5 = h5py.File(os.path.join(datadir, str(n)+"_edges.h5"))
    keys_gas = list(fh5.keys())[ns_gas*n_faces:(ns_gas+1)*n_faces]
    keys_dust_0 = list(fh5.keys())[ns_dust_0*n_faces:(ns_dust_0+1)*n_faces]
    keys_dust_1 = list(fh5.keys())[ns_dust_1*n_faces:(ns_dust_1+1)*n_faces]
    keys_dust_2 = list(fh5.keys())[ns_dust_2*n_faces:(ns_dust_2+1)*n_faces]
    keys_dust_3 = list(fh5.keys())[ns_dust_3*n_faces:(ns_dust_3+1)*n_faces]
    head = fh5.attrs
    nx, ny, nz = head["dims"]
    dx, dy, dz = head["dx"]
    t = head["t"]

    rates_cloud, rates_dust_0, rates_dust_1, rates_dust_2, rates_dust_3 = [], [], [], [], []
    for i, key in enumerate(keys_gas):
        velocity, mask = None, None

        gas = fh5[keys_gas[i]][()]
        dust_0 = fh5[keys_dust_0[i]][()]
        dust_1 = fh5[keys_dust_1[i]][()]
        dust_2 = fh5[keys_dust_2[i]][()]
        dust_3 = fh5[keys_dust_3[i]][()]

        if i <= 2:
            velocity = fh5[ms[i]] / gas
            mask = np.logical_and(gas >= cutoff, velocity < 0)
        if i > 2:
            velocity = fh5[ms[i]] / gas
            mask = np.logical_and(gas >= cutoff, velocity > 0)  

        rates_cloud.append(calc_mass_loss_rate(gas[mask], velocity[mask], dx**2))

        if i <= 2:
            velocity = fh5[ms[i]] / gas
            mask = np.logical_and(dust_0 >= 0, velocity < 0)
        if i > 2:
            velocity = fh5[ms[i]] / gas
            mask = np.logical_and(dust_0 >= 0, velocity > 0)
        
        rates_dust_0.append(calc_mass_loss_rate(dust_0[mask], velocity[mask], dx**2))

        if i <= 2:
            velocity = fh5[ms[i]] / gas
            mask = np.logical_and(dust_1 >= 0, velocity < 0)
        if i > 2:
            velocity = fh5[ms[i]] / gas
            mask = np.logical_and(dust_1 >= 0, velocity > 0)

        rates_dust_1.append(calc_mass_loss_rate(dust_1[mask], velocity[mask], dx**2))

        if i <= 2:
            velocity = fh5[ms[i]] / gas
            mask = np.logical_and(dust_2 >= 0, velocity < 0)
        if i > 2:
            velocity = fh5[ms[i]] / gas
            mask = np.logical_and(dust_2 >= 0, velocity > 0)

        rates_dust_2.append(calc_mass_loss_rate(dust_2[mask], velocity[mask], dx**2))

        if i <= 2:
            velocity = fh5[ms[i]] / gas
            mask = np.logical_and(dust_3 >= 0, velocity < 0)
        if i > 2:
            velocity = fh5[ms[i]] / gas
            mask = np.logical_and(dust_3 >= 0, velocity > 0)

        rates_dust_3.append(calc_mass_loss_rate(dust_3[mask], velocity[mask], dx**2))

    with open(os.path.join(csvdir, cloud_csv_str), "a") as f:
        writer_obj = writer(f)
        writer_obj.writerow(rates_cloud)
        f.close()

    with open(os.path.join(csvdir, dust_0_csv_str), "a") as f:
        writer_obj = writer(f)
        writer_obj.writerow(rates_dust_0)
        f.close()

    with open(os.path.join(csvdir, dust_1_csv_str), "a") as f:
        writer_obj = writer(f)
        writer_obj.writerow(rates_dust_1)
        f.close()

    with open(os.path.join(csvdir, dust_2_csv_str), "a") as f:
        writer_obj = writer(f)
        writer_obj.writerow(rates_dust_2)
        f.close()

    with open(os.path.join(csvdir, dust_3_csv_str), "a") as f:
        writer_obj = writer(f)
        writer_obj.writerow(rates_dust_3)
        f.close()

    with open(os.path.join(csvdir, time_csv_str), "a") as f:
        writer_obj = writer(f)
        writer_obj.writerow(t)
        f.close()
