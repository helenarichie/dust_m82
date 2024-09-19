import sys
sys.path.insert(0, "/ix/eschneider/helena/code/my_scripts/")
from hconfig import *
from csv import writer

date = "2024-08-28"

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

f = open(os.path.join(csvdir, "sputtered_0.csv"), "w")
f.close()
f = open(os.path.join(csvdir, "sputtered_1.csv"), "w")
f.close()
f = open(os.path.join(csvdir, "sputtered_2.csv"), "w")
f.close()
f = open(os.path.join(csvdir, "sputtered_3.csv"), "w")
f.close()
f = open(os.path.join(csvdir, "dust_0.csv"), "w")
f.close()
f = open(os.path.join(csvdir, "dust_1.csv"), "w")
f.close()
f = open(os.path.join(csvdir, "dust_2.csv"), "w")
f.close()
f = open(os.path.join(csvdir, "dust_3.csv"), "w")
f.close()
f = open(os.path.join(csvdir, "gas.csv"), "w")
f.close()

times = []
times_counter = 0

row_sputtered_0 = np.zeros((10, 4))
row_sputtered_1 = np.zeros((10, 4))
row_sputtered_2 = np.zeros((10, 4))
row_sputtered_3 = np.zeros((10, 4))
row_dust_0 = np.zeros((10, 4))
row_dust_1 = np.zeros((10, 4))
row_dust_2 = np.zeros((10, 4))
row_dust_3 = np.zeros((10, 4))
row_gas = np.zeros((10, 4))

f = open(os.path.join(csvdir, "m82_fixed.log"), "w")
f.close()

with open(os.path.join("m82_output_copy.log")) as f:
    sub_str = "Average"
    counter = 0
    for line in f:
        # print(line)
        if sub_str in line:
            line = line[:line.find(sub_str)]
            with open(os.path.join(csvdir, "m82_fixed.log"), "a") as f_txt:
                    f_txt.write(line)
                    f_txt.close()
            counter = 2
            continue
        if counter != 0:
            counter -= 1
            continue
        with open(os.path.join(csvdir, "m82_fixed.log"), "a") as f_txt:
                f_txt.write(line.lstrip())
                f_txt.close()