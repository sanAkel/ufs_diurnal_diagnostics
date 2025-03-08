#!/usr/bin/env python3

import os
import sys
import subprocess
import pandas as pd

import warnings
warnings.filterwarnings('ignore') 
# --
#
# Following way to set inputs is nasty! Should be yaml-ized as in:
# https://github.com/sanAkel/ufs_diurnal_diagnostics/blob/main/RTOFS/score-card/data-prep/get_files.py
#
exp_name = 'HR5-winter'
exp_type = "gfs"
start_date, end_date = ['2019-12-03', '2020-02-25'] # 00UTC
days_skip = "3D"

hpss_path = "/NCEPDEV/emc-climate/5year/role.ufscpara/WCOSS2/HR5/winter/"
tar_fName = "ocean_6hravg.tar"
extract_suff = "/00/model/ocean/history/gfs.ocean.t00z.6hr_avg.f*.nc"

output_dir = "/scratch1/NCEPDEV/stmp2/Santha.Akella/data/HR5/" + "data_prepared/"
# --

print("\n=================")
print("Must: ")
print("module load hpss")
print("for this to work!")
print("=================\n")

cwd = os.getcwd()
print("Current path:\n{}\n".format(cwd))

# Path to save files from HPSS
oPath = output_dir + exp_name
if not os.path.exists( oPath):
  print(f'\nOutput path:\t{oPath}\t does not exist. Creating it.\n')
  subprocess.run( ["mkdir", "-p", "{}".format(oPath)], check=True, capture_output=True)
os.chdir( oPath)

# Fetch files
start_date, end_date = [pd.to_datetime(start_date), pd.to_datetime(end_date)]
for data_date in pd.date_range(start_date, end_date, freq=days_skip):
  inPath_str1 = hpss_path + "{}".format(data_date.strftime('%Y%m%d')) + "00/{}".format(tar_fName)
  inPath_str2 = exp_type + ".{}".format(data_date.strftime('%Y%m%d')) + extract_suff

  stat1 = os.system("htar -xvf " + inPath_str1 + " " + inPath_str2)
  if stat1 == 0:
    print("\nFetched files for {}\n".format(data_date.strftime('%Y%m%d')))
  else:
    sys.exit("Error on {}. Fix and try again.".format(data_date.strftime('%Y%m%d')))
