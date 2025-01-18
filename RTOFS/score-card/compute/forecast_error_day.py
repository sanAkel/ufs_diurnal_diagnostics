#!/usr/bin/env python3

import os
import sys
import glob as glob
import argparse
import pandas as pd
import xarray as xr

from utils import get_forecast_error

import warnings
warnings.filterwarnings('ignore') 
# --

# user inputs
get_inputs = argparse.ArgumentParser(prog='\nforecast_error_day.py',\
  description='Calculate forecast error for RTOFS: forecast minus nowcast', usage='%(prog)s [options]')

get_inputs.add_argument('--data_path_root', type=str,\
  help='path where nowcast and forecast files reside',\
  default='/collab1/data/Santha.Akella/RTOFS/score_card/')

get_inputs.add_argument('--exp_name', type=str,\
  help='Name of the experiment- should match path name',\
  default='v2.4')

get_inputs.add_argument('--proc_date', type=str,\
        help='Date for which forecast error is to be calculated',\
        metavar='example: 2024-11-07',\
        required=True)

get_inputs.add_argument('--var_name_short', type=str,\
  help='Variable name, one of: s, t, u, v', required=True)

get_inputs.add_argument('--fcst_nDays', type=int,\
  help='Number of days up to which forecast is available', default=8)

get_inputs.add_argument('--save_top_level', action='store_true',\
  help='Save error at the top level (z=10 m), False if flag is absent')

get_inputs.add_argument('--save_mean_only', action='store_true',\
  help='Save only the mean error, False if flag is absent')

get_inputs.add_argument('--output_data_path_root', type=str,\
  help='path where forecast error files are to be saved',\
  default='/collab1/data/Santha.Akella/RTOFS/score_card/fcst_err/')

# Following are fixed for RTOFS
get_inputs.add_argument('--forecast_file_pref', type=str,\
  help='RTOFS forecast files prefix', default='rtofs_glo_3dz_f')

get_inputs.add_argument('--nowcast_file_pref', type=str,\
  help='RTOFS nowcast files prefix', default='rtofs_glo_3dz_n024')

get_inputs.add_argument('--file_suff', type=str,\
  help='suffix of RTOFS nowcast/forecast files', default='io.nc')
  
args = get_inputs.parse_args()
# --

data_path_root = args.data_path_root
exp_name = args.exp_name
proc_date = args.proc_date
save_top_level = args.save_top_level
save_mean_only = args.save_mean_only
output_data_path_root = args.output_data_path_root
fcst_nDays = args.fcst_nDays
var_names = args.var_name_short
forecast_file_pref = args.forecast_file_pref
nowcast_file_pref  = args.nowcast_file_pref
file_suff = args.file_suff
# --

data_date =  pd.to_datetime(proc_date)
data_date_str = data_date.strftime("%Y%m%d")

for var in var_names:

  # get fcst_err = fcst - anal, it is 4-D dataset: 3d + forecast duration (8-days) 
  [fcst_fNames, anal_fNames, fcst_err] = get_forecast_error( proc_date, data_path_root, exp_name, \
  forecast_file_pref, nowcast_file_pref, var, file_suff)

  var_name = list(fcst_err.keys())
  print("Differencing:\t{}".format(var_name))
  
  if (save_mean_only):
    glb_mean = fcst_err[var_name].mean( ('Y', 'X'))

  glb_sdev = fcst_err[var_name].std( ('Y', 'X'))

  # Save output file(s)
  fName_fcst_err_pref = output_data_path_root + '{}/'.format(exp_name) + data_date_str
  if (save_top_level):
    fcst_err.isel(Depth=0).compute().to_netcdf( fName_fcst_err_pref +'_top_lev_fcst_err_'+ var + '.nc')
  
  # set `HDF5_USE_FILE_LOCKING=FALSE` to safely write following?
  if (save_mean_only):
    glb_mean.compute().to_netcdf( fName_fcst_err_pref +'_glob_mean_fcst_err_'+ var + '.nc')

  glb_sdev.compute().to_netcdf( fName_fcst_err_pref +'_glob_sdev_fcst_err_'+ var + '.nc')
