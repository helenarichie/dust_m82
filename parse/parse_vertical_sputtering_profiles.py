###############################
crc = False
frontier = False
mypc = True
###############################

from csv import writer
import sys
import os
if crc:
    sys.path.insert(0, "/ix/eschneider/helena/code/my_scripts/")
if mypc:
    sys.path.insert(0, "/Users/helenarichie/GitHub/my_scripts/")
from hconfig import *

date = "2024-10-25"
tmaxs = np.linspace(0, 50000, 101)

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

fields = ["sputtered_0", "sputtered_1", "sputtered_2", "sputtered_3"]
labels = ["hot", "mixed", "cool"]

for field in fields:
    f = open(os.path.join(csvdir, f"{field}_hot_short.csv"), "w")
    f.close()
    f = open(os.path.join(csvdir, f"{field}_mixed_short.csv"), "w")
    f.close()
    f = open(os.path.join(csvdir, f"{field}_cool_short.csv"), "w")
    f.close()

for s, field in enumerate(fields):
    print(field)
    breakout = False
    tmax_i = 0
    sputtered = np.zeros((4, 10, 3))
    with open(os.path.join(csvdir, f"{field}.csv")) as f:
        for line in f:
            line = line.split(",")
            for i, bin in enumerate(line):
                bin = bin.replace("[", "")
                bin = bin.replace("]", "")
                bin = bin.split(" ")
                while("" in bin):
                    bin.remove("")
                if i < 10:
                    sputtered[s][i] = sputtered[s][i] + np.array(bin[1:4], dtype=float)
                    time = float(bin[0])
            if time == tmaxs[tmax_i]:
                for j in range(0, 2+1):
                    row = [tmaxs[tmax_i]]
                    for sput in sputtered[s][:,j]:
                        row.append(sput)
                    with open(os.path.join(csvdir, f"{field}_{labels[j]}_short.csv"), "a") as f_write:
                        writer_obj = writer(f_write)
                        writer_obj.writerow(row)
                        f_write.close()
                if tmax_i < (len(tmaxs)-1):
                    tmax_i += 1
                else:
                    breakout = True
                    break
            if breakout:
                break