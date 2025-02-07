import argparse
import numpy as np
import os
import sys
import pathlib
sys.path.insert(0, os.path.join(pathlib.Path(__file__).parent.resolve(), "../utils/"))
from calc_tau_sp import calc_tau_sp

def read_cmdline():
    p = argparse.ArgumentParser()
    p.add_argument("-a", "--grain-radius", type=float, required=True)
    p.add_argument("-t", "--temperature", type=float, required=True)
    p.add_argument("-n", "--number-density", type=float, required=True)
    args = p.parse_args()
    return args

def main(a, T, n):
    
    print(f"\ntau_sp({n} cm^-3, {T:.2e} K, {a*0.1} micron) = {calc_tau_sp(n, T, a):.4e} yr\n")

if __name__ == "__main__":
    args = read_cmdline()

    a = args.grain_radius
    T = args.temperature
    n = args.number_density

    main(a, T, n)
