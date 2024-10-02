#!/usr/bin/env python3

import sys
import os
import subprocess
import argparse
import xarray as xr

# Gather output from SFS experiment(s) listed at:
# https://docs.google.com/spreadsheets/d/1ZaPhs1-0DTA7e_CrPULGJumevea6IXjk2xw1p-jbYdc/edit?gid=0#gid=0
# Below options were coded with what was available as of October 02, 2024.
# --

def get_data_path(exp_name="SFS_Baseline"):

  if exp_name == "Proof_of_concept":
    data_path = "/scratch1/BMC/isp-1/UFS/v16p8/stmp2/Archive/P8c2_IC_Runs/IC_10-01s/"
  elif exp_name == "P8":
    data_path = "/ESRL/BMC/fim/5year/Shan.Sun/p81deg_oras5/"
  elif exp_name == "SFS_Baseline":
    data_path = "/ESRL/BMC/fim/5year/Shan.Sun/hr4hydro_20240726/c96mx100/19940501/"
  else:
    sys.exit("\nUnknown or invalid SFS experiment name:\t{}\nFix and try again\n\n".format(exp_name))

  return data_path
# --

# User inputs
get_inputs = argparse.ArgumentParser(prog='\n"gather_exp_output.py"',\
description='To gather data from HPSS archive', usage='%(prog)s [options]',\
formatter_class=argparse.ArgumentDefaultsHelpFormatter)

get_inputs.add_argument('--exp_name', type=str,\
                        metavar='Name of the experiment',\
                        help="Either from OAR labs or EMC", default="SFS_Baseline")
# year, month
# filePref, fileSuff

get_inputs.add_argument('--output_dir', type=str,\
                        metavar='Name of the directory where output will go',\
                        help="This should be in-sync with your .gitignore", default="data")
args = get_inputs.parse_args()
# --

sfs_path = get_data_path(args.exp_name)
print("\nGathering data in path:\n{}\n".format(sfs_path))

# Create dir that will hold data (temporarily)
cwd = os.getcwd()
if not os.path.exists(cwd+"/"+args.output_dir):
  stat = subprocess.run(["mkdir", "-p", args.output_dir], check=False, capture_output=False)
  if stat.returncode == 0:
    print("\nGathered data will be saved to:\n{}\n".format(cwd+"/"+args.output_dir))

