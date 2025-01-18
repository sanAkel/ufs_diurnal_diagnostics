#!/usr/bin/env python3

import os
import sys
import glob as glob
import argparse
import numpy as np
import pandas as pd
import xarray as xr

from utils import get_forecast_error

import warnings
warnings.filterwarnings('ignore') 
# --

# user inputs
get_inputs = argparse.ArgumentParser(prog='\ncalculate_3d_stat_fcst_err.py',\
  description='Calculate mean and standard deviation of forecast errors', usage='%(prog)s [options]')

get_inputs.add_argument('--data_path_root', type=str,\
  help='path where nowcast and forecast files reside',\
  default='/collab1/data/Santha.Akella/RTOFS/score_card/')

get_inputs.add_argument('--exp_name', type=str,\
  help='Name of the experiment- should match path name',\
  default='v2.4')

get_inputs.add_argument('--var_name_short', type=str,\
  help='Variable name, one of: s, t, u, v', required=True)

get_inputs.add_argument('--start_date', type=str,\
        help='Start date for calculating error statistics',\
        metavar='example: 2024-11-15', default='2024-11-15')

get_inputs.add_argument('--end_date', type=str,\
        help='End date for calculating error statistics',\
        metavar='example: 2024-12-24', default='2024-12-24')

get_inputs.add_argument('--fcst_nDays', type=int,\
  help='Number of days up to which each forecast is available', default=8)

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
var_name_short = args.var_name_short
start_date = pd.to_datetime(args.start_date)
end_date = pd.to_datetime(args.end_date)

fcst_nDays = args.fcst_nDays
output_data_path_root = args.output_data_path_root
forecast_file_pref = args.forecast_file_pref
nowcast_file_pref  = args.nowcast_file_pref
file_suff = args.file_suff
# --


# -- 1. Calculate mean

nSamples = 0
for data_date in pd.date_range(start_date, end_date):

  data_date_str = data_date.strftime("%Y-%m-%d")
  print(data_date_str)
  # get fcst_err = fcst - anal, it is 4-D dataset: 3d + forecast duration (8-days) 
  [fcst_fNames, anal_fNames, fcst_err] = get_forecast_error( data_date, data_path_root, exp_name, \
  forecast_file_pref, nowcast_file_pref, var_name_short, file_suff)

  if nSamples == 0:
    varable_name_long = list(fcst_err.keys())
    print("Differencing:\t{}".format(varable_name_long))
    cumSum = fcst_err
  else:
    cumSum = cumSum + fcst_err

  nSamples +=1

mean_fcst_err = (cumSum/nSamples).compute()
print(f'Calculated 3D mean forecast error using\t {nSamples} samples.')

# -- 2. Calculate standard deviation
print('\nNext calculating standard deviation around this mean.\n')

nSamples = 0
for data_date in pd.date_range(start_date, end_date):

  data_date_str = data_date.strftime("%Y-%m-%d")
  print(data_date_str)
  # get fcst_err = fcst - anal, it is 4-D dataset: 3d + forecast duration (8-days) 
  [fcst_fNames, anal_fNames, fcst_err] = get_forecast_error( data_date, data_path_root, exp_name, \
  forecast_file_pref, nowcast_file_pref, var_name_short, file_suff)

  if nSamples == 0:
    varable_name_long = list(fcst_err.keys())
    print("Differencing:\t{}".format(varable_name_long))
    cumSum = (fcst_err-mean_fcst_err)**2
  else:
    cumSum = cumSum + (fcst_err-mean_fcst_err)**2

  nSamples +=1

sdev_fcst_err = np.sqrt( cumSum/(nSamples-1))
print(f'Dask calculated 3D standard deviation of forecast error using\t {nSamples} samples.')
# -- 

# Save output file(s)
fName_mean = output_data_path_root + '{}/'.format(exp_name) +\
  '3d_mean_{}_{}_{}.nc'.format(var_name_short, start_date.strftime("%Y%m%d"), end_date.strftime("%Y%m%d"))

fName_sdev = output_data_path_root + '{}/'.format(exp_name) +\
  '3d_sdev_{}_{}_{}.nc'.format(var_name_short, start_date.strftime("%Y%m%d"), end_date.strftime("%Y%m%d"))
  
print(f'Saving averaged field to:\n{fName_mean}\n This may take some time.')
mean_fcst_err.to_netcdf( fName_mean)

print(f'Calculating and saving standard deviation to:\n{fName_sdev}\n Be patient!')
sdev_fcst_err.compute().to_netcdf( fName_sdev)
