#!/usr/bin/env python3

"""
- Use the data that was extracted from HPSS
(via https://github.com/sanAkel/ufs_diurnal_diagnostics/blob/main/GFS/regional_diagnostics/get_hpss_files.py)

- Cull out variables to keep those specified by the user.

- Save data to file for plotting (via another script).
"""

import os
import sys
import subprocess
import pandas as pd
import xarray as xr

import warnings
warnings.filterwarnings('ignore') 
# --
#
# Following way to set inputs is nasty! Should be yaml-ized as in:
# https://github.com/sanAkel/ufs_diurnal_diagnostics/blob/main/RTOFS/score-card/data-prep/get_files.py
#
exp_name = 'HR5-winter'
exp_type = "gfs"
fcst_start_date, fcst_end_date = ['2019-12-03', '2019-12-30'] # 00UTC
fcst_days_skip = "3D"
fcst_dir_suff = "/00/model/ocean/history/"
fcst_file_pref = "gfs.ocean.t00z.6hr_avg.f"
fcst_file_suff = ".nc"
vars_to_extract = ["SST", "SSS", "geolon", "geolat"] # must match names of variables in netcdf file: needs prior inspection or diag_table of model run.

fcst_dir_pre = "/scratch1/NCEPDEV/stmp2/Santha.Akella/data/HR5/" +\
               "data_prepared/" + exp_name + "/"

# --

# Read, cull, save
start_date, end_date = [pd.to_datetime(fcst_start_date), pd.to_datetime(fcst_end_date)]
for data_date in pd.date_range(start_date, end_date, freq=fcst_days_skip):
  input_dir = fcst_dir_pre + "{}.{}/".format(exp_type, data_date.strftime('%Y%m%d')) + fcst_dir_suff
  print(f'Reading data from:\t{input_dir}')

  # Read all files
  ds = xr.open_mfdataset(input_dir+ fcst_file_pref + "*" + fcst_file_suff)

  # Cull variables and keep user specified ones only
  ds_culled = ds[vars_to_extract]

  # Save to a (new) file
  fName = fcst_dir_pre +\
          exp_name + "_post_proc_{}".format(data_date.strftime('%Y%m%d')) + fcst_file_suff
  ds_culled.to_netcdf(fName)
  print(f'Saved data to:\t{fName}')
  print("\n")
