###############################
crc = False
frontier = False
mypc = True
###############################

from csv import writer
import sys
import seaborn as sns
import os
if crc:
    sys.path.insert(0, "/ix/eschneider/helena/code/my_scripts/")
if mypc:
    sys.path.insert(0, "/Users/helenarichie/GitHub/my_scripts/")
from hconfig import *

date = "2024-10-25"
no_disk = True
disk_i = 1
fields = ["dust_1", "dust_2", "dust_3"]

########## data type ############
debugging = False
cloud_wind = False
testing = False
m82 = True
#################################

if crc:
  if debugging:
      basedir = f"/ix/eschneider/helena/data/debugging/{date}/"
  if cloud_wind:
      basedir = f"/ix/eschneider/helena/data/cloud_wind/{date}/"
  if testing:
      basedir = f"/ix/eschneider/helena/data/testing/{date}/"
  if m82:
      basedir = f"/ix/eschneider/helena/data/m82/{date}/"
if frontier:
  basedir = f"/lustre/orion/ast181/scratch/helenarichie/{date}/"
if mypc:
  basedir = f"/Users/helenarichie/Desktop/{date}/profiles/vertical/"

csvdir = os.path.join(basedir, "csv/")

d_arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
if no_disk:
    d_arr = d_arr[disk_i:]

sputtered_0_hot = []
sputtered_1_hot = []
sputtered_2_hot = []
sputtered_3_hot = []
sputtered_0_mixed = []
sputtered_1_mixed = []
sputtered_2_mixed = []
sputtered_3_mixed = []
sputtered_0_cool = []
sputtered_1_cool = []
sputtered_2_cool = []
sputtered_3_cool = []

with open(os.path.join(csvdir, f"sputtered_0_hot_short.csv"), "r") as f:
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        sputtered_0_hot.append(line)
f.close()
sputtered_0_hot = np.array(sputtered_0_hot, dtype=float)

with open(os.path.join(csvdir, f"sputtered_1_hot_short.csv"), "r") as f:
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        sputtered_1_hot.append(line)
f.close()
sputtered_1_hot = np.array(sputtered_1_hot, dtype=float)

with open(os.path.join(csvdir, f"sputtered_2_hot_short.csv"), "r") as f:
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        sputtered_2_hot.append(line)
f.close()
sputtered_2_hot = np.array(sputtered_2_hot, dtype=float)

with open(os.path.join(csvdir, f"sputtered_3_hot_short.csv"), "r") as f:
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        sputtered_3_hot.append(line)
f.close()
sputtered_3_hot = np.array(sputtered_3_hot, dtype=float)

with open(os.path.join(csvdir, f"sputtered_0_mixed_short.csv"), "r") as f:
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        sputtered_0_mixed.append(line)
f.close()
sputtered_0_mixed = np.array(sputtered_0_mixed, dtype=float)

with open(os.path.join(csvdir, f"sputtered_1_mixed_short.csv"), "r") as f:
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        sputtered_1_mixed.append(line)
f.close()
sputtered_1_mixed = np.array(sputtered_1_mixed, dtype=float)

with open(os.path.join(csvdir, f"sputtered_2_mixed_short.csv"), "r") as f:
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        sputtered_2_mixed.append(line)
f.close()
sputtered_2_mixed = np.array(sputtered_2_mixed, dtype=float)

with open(os.path.join(csvdir, f"sputtered_3_mixed_short.csv"), "r") as f:
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        sputtered_3_mixed.append(line)
f.close()
sputtered_3_mixed = np.array(sputtered_3_mixed, dtype=float)

with open(os.path.join(csvdir, f"sputtered_0_cool_short.csv"), "r") as f:
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        sputtered_0_cool.append(line)
f.close()
sputtered_0_cool = np.array(sputtered_0_cool, dtype=float)

with open(os.path.join(csvdir, f"sputtered_1_cool_short.csv"), "r") as f:
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        sputtered_1_cool.append(line)
f.close()
sputtered_1_cool = np.array(sputtered_1_cool, dtype=float)

with open(os.path.join(csvdir, f"sputtered_2_cool_short.csv"), "r") as f:
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        sputtered_2_cool.append(line)
f.close()
sputtered_2_cool = np.array(sputtered_2_cool, dtype=float)

with open(os.path.join(csvdir, f"sputtered_3_cool_short.csv"), "r") as f:
    for line in f:
        line = line.rstrip("\n")
        line = line.split(",")
        sputtered_3_cool.append(line)
f.close()
sputtered_3_cool = np.array(sputtered_3_cool, dtype=float)

##################################################################
basedir = f"/Users/helenarichie/Desktop/{date}/fluxes/"
pngdir = os.path.join(basedir, "png/")
csvdir = os.path.join(basedir, "csv/")
##################################################################

rates_hot = []
for field in fields:
    rate_i = []
    with open(os.path.join(csvdir, f"rate_{field}_hot_1e-24.csv")) as f:
        for line in f:
            line = line.split(",")
            rate_i.append(np.array(line, dtype=float))
    rates_hot.append(rate_i)

rates_mixed = []
for field in fields:
    rate_i = []
    with open(os.path.join(csvdir, f"rate_{field}_mixed_1e-24.csv")) as f:
        for line in f:
            line = line.split(",")
            rate_i.append(np.array(line, dtype=float))
    rates_mixed.append(rate_i)

rates_cool = []
for field in fields:
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
time_output = np.array(time_output)

dt_out = time_output[2] - time_output[1]

mass_out_hot = []
for rate in rates_hot:
    mass_out_i = []
    mass_cumulative = 0
    for i, rate_i in enumerate(rate):
        rate_i = np.sum(rate_i)
        mass_cumulative += rate_i * dt_out
        mass_out_i.append(mass_cumulative)
    mass_out_hot.append(mass_out_i)
mass_out_hot = np.array(mass_out_hot)

mass_out_mixed = []
for rate in rates_mixed:
    mass_out_i = []
    mass_cumulative = 0
    for i, rate_i in enumerate(rate):
        rate_i = np.sum(rate_i)
        mass_cumulative += rate_i * dt_out
        mass_out_i.append(mass_cumulative)
    mass_out_mixed.append(mass_out_i)
mass_out_mixed = np.array(mass_out_mixed)

mass_out_cool = []
for rate in rates_cool:
    mass_out_i = []
    mass_cumulative = 0
    for i, rate_i in enumerate(rate):
        rate_i = np.sum(rate_i)
        mass_cumulative += rate_i * dt_out
        mass_out_i.append(mass_cumulative)
    mass_out_cool.append(mass_out_i)
mass_out_cool = np.array(mass_out_cool)

sput_ind = np.where(sputtered_0_cool[:,0]==30e3)[0][0]
outflow_ind = np.where(time_output==30e3)[0][0]

hot_outflow_1 = np.sum(mass_out_hot[0][outflow_ind])
hot_outflow_2 = np.sum(mass_out_hot[1][outflow_ind])
hot_outflow_3 = np.sum(mass_out_hot[2][outflow_ind])
mixed_outflow_1 = np.sum(mass_out_mixed[0][outflow_ind])
mixed_outflow_2 = np.sum(mass_out_mixed[1][outflow_ind])
mixed_outflow_3 = np.sum(mass_out_mixed[2][outflow_ind])
cool_outflow_1 = np.sum(mass_out_cool[0][outflow_ind])
cool_outflow_2 = np.sum(mass_out_cool[1][outflow_ind])
cool_outflow_3 = np.sum(mass_out_cool[2][outflow_ind])

hot_sput_1 = np.sum(sputtered_1_hot[sput_ind][disk_i+1:])
hot_sput_2 = np.sum(sputtered_2_hot[sput_ind][disk_i+1:])
hot_sput_3 = np.sum(sputtered_3_hot[sput_ind][disk_i+1:])
mixed_sput_1 = np.sum(sputtered_1_mixed[sput_ind][disk_i+1:])
mixed_sput_2 = np.sum(sputtered_2_mixed[sput_ind][disk_i+1:])
mixed_sput_3 = np.sum(sputtered_3_mixed[sput_ind][disk_i+1:])
cool_sput_1 = np.sum(sputtered_1_cool[sput_ind][disk_i+1:])
cool_sput_2 = np.sum(sputtered_2_cool[sput_ind][disk_i+1:])
cool_sput_3 = np.sum(sputtered_3_cool[sput_ind][disk_i+1:])

# print(f"0.1 micron hot-phase mass outflow: {hot_outflow_1:.2e}")
# print(f"0.01 micron hot-phase mass outflow: {hot_outflow_2:.2e}")
# print(f"0.001 micron hot-phase mass outflow: {hot_outflow_3:.2e}")

# print(f"0.1 micron hot-phase sputtering: {hot_sput_1:.2e}")
# print(f"0.01 micron hot-phase sputtering: {hot_sput_2:.2e}")
# print(f"0.001 micron hot-phase sputtering: {hot_sput_3:.2e}")

# sputtered + outflow
total_1 = hot_sput_1 + mixed_sput_1 + cool_sput_1 + hot_outflow_1 + mixed_outflow_1 + cool_outflow_1
survived_1 = hot_outflow_1 + mixed_outflow_1 + cool_outflow_1
print(f"0.1 micron fraction: {(survived_1/total_1):.2}")

total_2 = hot_sput_2 + mixed_sput_2 + cool_sput_2 + hot_outflow_2 + mixed_outflow_2 + cool_outflow_2
survived_2 = hot_outflow_2 + mixed_outflow_2 + cool_outflow_2
print(f"0.01 micron fraction: {(survived_2/total_2):.2}")

total_3 = hot_sput_3 + mixed_sput_3 + cool_sput_3 + hot_outflow_3 + mixed_outflow_3 + cool_outflow_3
survived_3 = hot_outflow_3 + mixed_outflow_3 + cool_outflow_3
print(f"0.001 micron fraction: {(survived_3/total_3):.2}")