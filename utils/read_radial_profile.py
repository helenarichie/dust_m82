import os
import numpy as np

def read_radial_profile(basedir, fnum, simulation, phase, weight, tail=None):
    N_bins = 80

    f_name = f"{fnum}_prof_{simulation}_{phase}_{weight}{tail}.txt"

    parse_totals = False
    parse_stats = False

    bin_tot = []
    m_gas = []
    m_dust_0 = []
    m_dust_1 = []
    m_dust_2 = []
    m_dust_3 = []

    cell_count = []
    gas_avg = []
    gas_med = []
    gas_lo = []
    gas_hi = []
    temp_avg = []
    temp_med = []
    temp_lo = []
    temp_hi = []
    v_avg = []
    v_med = []
    v_lo = []
    v_hi = []
    P_avg = []
    P_med = []
    P_lo = []
    P_hi = []
    S_avg = []
    S_med = []
    S_lo = []
    S_hi = []
    M_avg = []
    M_med = []
    M_lo = []
    M_hi = []

    with open(os.path.join(basedir, f_name)) as f:
        line_i = 0
        for line in f:
            if parse_totals:
                line_i += 1
                line = line.strip(" ").rstrip("\n").split(",")
                bin_tot.append(float(line[0]))
                m_gas.append(float(line[1]))
                m_dust_0.append(float(line[2]))
                m_dust_1.append(float(line[3]))
                m_dust_2.append(float(line[4]))
                m_dust_3.append(float(line[5]))
                if line_i == N_bins:
                    parse_totals = False
                    line_i = 0
            
            elif parse_stats:
                line_i += 1
                line = line.rstrip("\n").split(",")
                for i, entry in enumerate(line):
                    if i == 1:
                        entry = entry.strip(" ")
                        cell_count.append(int(entry[0]))
                    if i == 2:
                        entry = entry.split(" ")
                        while("" in entry):
                            entry.remove("")
                        gas_avg.append(float(entry[1]))
                        gas_med.append(float(entry[2]))
                        gas_lo.append(float(entry[3]))
                        gas_hi.append(float(entry[4]))
                    if i == 3:
                        entry = entry.split(" ")
                        while("" in entry):
                            entry.remove("")
                        v_avg.append(float(entry[0]))
                        v_med.append(float(entry[1]))
                        v_lo.append(float(entry[2]))
                        v_hi.append(float(entry[3]))
                    if i == 4:
                        entry = entry.split(" ")
                        while("" in entry):
                            entry.remove("")
                        temp_avg.append(float(entry[0]))
                        temp_med.append(float(entry[1]))
                        temp_lo.append(float(entry[2]))
                        temp_hi.append(float(entry[3]))
                    if i == 5:
                        entry = entry.split(" ")
                        while("" in entry):
                            entry.remove("")
                        P_avg.append(float(entry[0]))
                        P_med.append(float(entry[1]))
                        P_lo.append(float(entry[2]))
                        P_hi.append(float(entry[3]))
                    if i == 6:
                        entry = entry.split(" ")
                        while("" in entry):
                            entry.remove("")
                        S_avg.append(float(entry[0]))
                        S_med.append(float(entry[1]))
                        S_lo.append(float(entry[2]))
                        S_hi.append(float(entry[3]))
                    if i == 7:
                        entry = entry.split(" ")
                        while("" in entry):
                            entry.remove("")
                        M_avg.append(float(entry[0]))
                        M_med.append(float(entry[1]))
                        M_lo.append(float(entry[2]))
                        M_hi.append(float(entry[3]))
                if line_i == N_bins:
                    parse_stats = False
                    line_i = 0 
            else:
                if line.startswith("# Totals:"):
                    parse_totals = True
                if line.startswith("# Statistics:"):
                    parse_totals = False
                    parse_stats = True
    
        m_dust = np.array([m_dust_0, m_dust_1, m_dust_2, m_dust_3])
        gas_density = np.array([gas_avg, gas_med, gas_lo, gas_hi])
        temperature = np.array([temp_avg, temp_med, temp_lo, temp_hi])
        velocity = np.array([v_avg, v_med, v_lo, v_hi])
        pressure = np.array([P_avg, P_med, P_lo, P_hi])
        entropy = np.array([S_avg, S_med, S_lo, S_hi])
        mach = np.array([M_avg, M_med, M_lo, M_hi])

    return bin_tot, m_gas, m_dust, gas_density, cell_count, temperature, velocity, pressure, entropy, mach