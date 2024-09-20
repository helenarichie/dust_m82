import sys
sys.path.insert(0, "/ix/eschneider/helena/code/my_scripts/")
from hconfig import *
from csv import writer

date = "2024-08-29"

###############################
crc = True
frontier = False
###############################

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

csvdir = os.path.join(basedir, "csv/")

f = open(os.path.join(csvdir, "high_z_fixed.log"), "w")
f.close()

with open(os.path.join(basedir, "output.log")) as f:
    sub_str = "Average"
    counter = 0
    for line in f:
        # print(line)
        if sub_str in line:
            line = line[:line.find(sub_str)]
            with open(os.path.join(csvdir, "high_z_fixed.log"), "a") as f_txt:
                    f_txt.write(line)
                    f_txt.close()
            counter = 2
            continue
        if counter != 0:
            counter -= 1
            continue
        with open(os.path.join(csvdir, "high_z_fixed.log"), "a") as f_txt:
                f_txt.write(line.lstrip())
                f_txt.close()