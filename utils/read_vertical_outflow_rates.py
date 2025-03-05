import os
import numpy as np

def read_vertical_outflow_rates(csvdir, field_names):
    rates_hot = []
    rates_mixed = []
    rates_cool = []
    time_output = []

    for field in field_names:
        rate_i = []
        with open(os.path.join(csvdir, f"rate_{field}_hot_1e-24.csv")) as f:
            for line in f:
                line = line.split(",")
                rate_i.append(np.array(line, dtype=float))
        rates_hot.append(rate_i)

        rate_i = []
        with open(os.path.join(csvdir, f"rate_{field}_mixed_1e-24.csv")) as f:
            for line in f:
                line = line.split(",")
                rate_i.append(np.array(line, dtype=float))
        rates_mixed.append(rate_i)

        rate_i = []
        with open(os.path.join(csvdir, f"rate_{field}_cool_1e-24.csv")) as f:
            for line in f:
                line = line.split(",")
                rate_i.append(np.array(line, dtype=float))
        rates_cool.append(rate_i)

        time_output = []
        with open(os.path.join(csvdir, "time_output_1e-24.csv")) as f:
            for line in f:
                time_output.append(float(line))

    rates_hot = np.array(rates_hot)
    rates_mixed = np.array(rates_mixed)
    rates_cool = np.array(rates_cool)
    time_output = np.array(time_output)

    return time_output, rates_hot, rates_mixed, rates_cool