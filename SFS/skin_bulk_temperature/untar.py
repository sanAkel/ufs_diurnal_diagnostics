#!/usr/bin/env python3

import os
import sys
import subprocess
import pandas as pd

# --
# yaml'ize: config.untar.yaml
data_path = "/collab1/data/Santha.Akella/skinSST_vs_NSST/data/"
exp_name = "c96mx100_mem000"
file_type = "_atm_raw_sfcf_"
file_suff = ".tar"
# --

start_date, end_date = ['1994-05-01', '2023-05-01']

exp_dates=pd.date_range(start_date, end_date, freq='12MS')

cwd = os.getcwd()
for dd in exp_dates:

  dStr=dd.strftime('%Y%m%d')
  dPathTarFile=data_path+exp_name+'_'+dStr+'/'

  # Untar the file
  if os.path.exists(dPathTarFile):
    os.chdir(dPathTarFile)
    #print('{}'.format(os.getcwd()))

    fName = exp_name + file_type + "{}".format(dStr) + file_suff
    print("Untar:\n{}".format(fName))

    stat1 = subprocess.run( ["tar", "-xvf", "{}".format(fName)], check=True, capture_output=True)
    if stat1.returncode == 0:
      # done with tar file, delete it.
      stat2 = subprocess.run( ["rm", "-f", "{}".format(fName)], check=True, capture_output=True)
      if stat2.returncode == 0:
        print("Purged tar file:\t{}\t".format(fName))
    else:
      sys.exit("Error in untar of:\n{}".format(dPathTarFile))
  else:
    sys.exit("Inaccessible path:\n{}\nFix and try again.".format(dPathTarFile))
  print("\n")
