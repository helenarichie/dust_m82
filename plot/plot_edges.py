import h5py
import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

###############################
date = "m82"
ns = 62
ne = 87
DE = True
SCALAR = True
###############################

###############################
crc = True
frontier = False
###############################

###############################
testing = True
cloud_wind = False
###############################

########### plotting #############
vlims = False
fontsize = 10
#################################

plt.rcParams.update({'font.family': 'Helvetica'})
plt.rcParams.update({'font.size': fontsize})

if crc:
  if cloud_wind:
    basedir = f"/ix/eschneider/helena/data/cloud_wind/{date}/"
  if testing:
    basedir = f"/ix/eschneider/helena/data/testing/{date}/"
  datadir = os.path.join(basedir, "hdf5/edges/")
  pngdir = os.path.join(basedir, "png/edges/")
if frontier:
  basedir = f"/lustre/orion/ast181/scratch/helenarichie/{date}/"
  datadir = os.path.join(basedir, "hdf5/edges/")
  pngdir = os.path.join(basedir, "png/edges/")

n_faces = 6
n_start = 3
key_nums = range(0, n_faces+1)

# loop over the output times
for n in range(ns, ne+1):
    f = h5py.File(os.path.join(datadir, str(n)+"_edges.h5"))
    keys = list(f.keys())[n_start*n_faces:(n_start+1)*n_faces]
    print(keys)
    head = f.attrs
    nx, ny, nz = head["dims"]
    dx, dy, dz = head["dx"]
    t = head["t"][0]

    fig, ax = plt.subplots(nrows=2, ncols=3)

    ax = ax.flatten()

    for i, key in enumerate(keys):
      data = f[key][()]

      im = ax[i].imshow(np.log10(data.T), origin="lower")
      ax[i].tick_params(axis='both', which='both', direction='in', color='black', top=1, right=1, length=8)
      fig.colorbar(im, ax=ax[i])
      ax[i].set_title(key, fontsize=fontsize)
    
    plt.tight_layout()
    plt.savefig(os.path.join(pngdir, str(n) + "_" + str(key) + "_edges.png"), dpi=300)
    plt.close()

    print(f"Saving figure {n} of {ne}.\n")
