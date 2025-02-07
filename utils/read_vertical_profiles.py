import os
import numpy as np

def read_vertical_profiles(csvdir, field_names):
    times = None
    mass_hot = []
    mass_mixed = []
    mass_cool = []
    for field in field_names:
        times = []
        mass_i = []
        with open(os.path.join(csvdir, f"{field}_hot_short.csv")) as f:
            for line in f:
                line = line.split(",")
                mass_i.append(np.array(line[1:], dtype=float))
                times.append(float(line[0]))
        mass_hot.append(mass_i)
        f.close()

        mass_i = []
        with open(os.path.join(csvdir, f"{field}_mixed_short.csv")) as f:
            for line in f:
                line = line.split(",")
                mass_i.append(np.array(line[1:], dtype=float))
        mass_mixed.append(mass_i)
        f.close()

        mass_i = []
        with open(os.path.join(csvdir, f"{field}_cool_short.csv")) as f:
            for line in f:
                line = line.split(",")
                mass_i.append(np.array(line[1:], dtype=float))
        mass_cool.append(mass_i)
        f.close()
    mass_hot = np.array(mass_hot)
    mass_mixed = np.array(mass_mixed)
    times = np.array(times)
    mass_cool = np.array(mass_cool)
    
    return times, mass_hot, mass_mixed, mass_cool