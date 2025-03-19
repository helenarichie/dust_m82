import h5py
import matplotlib.pyplot as plt
import numpy as np
import os
import pathlib
import sys
import seaborn as sns
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent.resolve(), "../utils/"))
from read_cmdline import read_cmdline

def main(basedir, outdir, fnum, field_names):
    for field_name in field_names:
        datadir = os.path.join(basedir, "hdf5", "proj")
        pngdir = os.path.join(basedir, "png")

        f = h5py.File(os.path.join(datadir, str(fnum)+"_proj.h5"), "r")    
        head = f.attrs
        nx, ny, nz = head["dims"][0], head["dims"][1], head["dims"][2]
        dx = head["dx"][0]

        field = np.array(f["d_" + f"{field_name}" + "_xz"])

        theta = np.pi / 6  # 30 degrees in radians
        bins = np.zeros(80)
        bin_count = np.zeros(80)
        dr = 0.125  # bin width in kpc

        mask = np.zeros((nx, nz), dtype=bool)
        
        for x_i in range(0, nx):
            for z_i in range(0, nz):
                x_coord, z_coord = x_i - nx / 2, z_i - nz / 2
                r = np.sqrt(x_coord ** 2 + z_coord ** 2)
                theta_i = np.arccos(abs(z_coord) / r)
                if theta_i < (theta):
                    print(theta_i, theta)
                    bin_i = r / dr
                    wh_bin = np.argmin(abs(bins - bin_i))
                    bins[wh_bin] += field[x_i, z_i]
                    bin_count[wh_bin] += 1
                else:
                    field[x_i, z_i] = 0

        # fig, ax = plt.subplots(1, 1)
        # cmap = sns.color_palette("rocket", as_cmap=True)
        # clabel = r'$\mathrm{log}_{10}(\Sigma_{dust})$ [$\mathrm{M}_\odot\,\mathrm{kpc}^{-2}$]'
        # im = ax.imshow(np.log10(field.T), origin="lower", vmin=0, vmax=8, extent=[0, nx*dx, 0, nz*dx], cmap=cmap)
        # fig.savefig(pngdir + f"/{fnum}.png", dpi=300, bbox_inches="tight")
        # plt.close()

        print(bins / bin_count)


if __name__ == "__main__":
    args = read_cmdline()

    sys.path.insert(0, args.configdir)
    import hconfig

    basedir = args.basedir
    outdir = args.outdir
    fnum = args.fnum
    field_names = args.field_names

    main(basedir, outdir, fnum, field_names)