import matplotlib.pyplot as plt
import numpy as np
import os
import pathlib
import sys
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent.resolve(), "../../utils/"))
from read_cmdline import read_cmdline

def main(outdir):
    distances = np.array([0.3748124373033481, 2.095583961111869, 11.722165859375771, 66.50119930808623, 372.04527293566287, 2113.5388407544983, 11790.943227587353, 66972.95686414257, 373881.6941106425, 2088037.573200979, 11868221.632906396, 66219741.345317066])
    densities = np.array([0.005101952250289417, 0.0024367977457989813, 0.001019990175175307, 0.0009423495649296874, 0.0003791373424660041, 0.00024207734900064627, 0.00020937118228565133,  0.0001390805744007113, 0.00010000000000000021, 0.00006469761215918919, 0.00003572799097214369, 0.000029701567487517446])

    av_distance = np.average(distances)
    av_density = np.average(densities)

    slope = np.sum((distances - av_distance) * (densities - av_density)) / np.sum((distances - av_distance)**2)
    intercept = av_density - slope * av_distance

    plt.loglog(distances, densities, marker="D", color="red")
    plt.xlabel("r [kpc]")
    plt.ylabel(r"$\Sigma_\mathrm{dust}$ $[h\,M_\odot/pc^2]$")

    plt.savefig(os.path.join(outdir, "menard.png"), dpi=300)

if __name__ == "__main__":
    args = read_cmdline()

    sys.path.insert(0, args.configdir)
    import hconfig

    outdir = args.outdir

    main(outdir)