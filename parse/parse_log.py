import sys
sys.path.insert(0, "/ix/eschneider/helena/code/my_scripts/")
from hconfig import *
from csv import writer

date = "m82"

###############################
crc = True
frontier = False
###############################

########## data type ############
debugging = False
cloud_wind = False
testing = True
m82 = False
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

with open(os.path.join(basedir, "output.log")) as f:
    for line in f:
        line_split = list(line)
        row_dust_0 = np.zeros((11, 3))
        row_dust_1 = np.zeros((11, 3))
        row_dust_2 = np.zeros((11, 3))
        row_dust_3 = np.zeros((11, 3))
        row_gas = np.zeros((11, 3))
        row_dust_0[:] = -1
        if line_split[0].isdigit():
            if line_split[3] == "S":
                line = line.replace("Sputtered mass:  (hot) ", "")
                line = line.replace("(mixed) ", "")
                line = line.replace("(cool) ", "")
                line.rstrip("\n")
                line = line.split("  ")
                for i in range(0, 10):
                    if line[0] == str(i):
                        row_dust_0[i+1] = [float(line[1]), float(line[5]), float(line[9])]
                        row_dust_1[i+1] = [float(line[2]), float(line[6]), float(line[10])]
                        row_dust_2[i+1] = [float(line[3]), float(line[7]), float(line[11])]
                        row_dust_3[i+1] = [float(line[4]), float(line[8]), float(line[12])]
        elif line.startswith("n_step"):
            line = line.split(" ")
            times.append(float(line[6]))
            row_dust_0[0] = [float(line[6]), float(line[6]), float(line[6])]
            row_dust_1[0] = [float(line[6]), float(line[6]), float(line[6])]
            row_dust_2[0] = [float(line[6]), float(line[6]), float(line[6])]
            row_dust_3[0] = [float(line[6]), float(line[6]), float(line[6])]
            with open(os.path.join(csvdir, "time.csv"), "a") as f_txt:
                writer_obj = writer(f_txt)
                writer_obj.writerow([times[times_counter]])
                times_counter += 1
                f_txt.close()