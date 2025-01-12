#!/usr/bin/env python3

import os
import sys
import glob as glob
import argparse
import pandas as pd
import xarray as xr

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

get_inputs.add_argument('--var_name', type=str,\
  help='Variable name, one of: s, t, u, v', required=True)

get_inputs.add_argument('--fcst_nDays', type=int,\
  help='Number of days up to which forecast is available', default=8)

get_inputs.add_argument('--save_top_level', action='store_true',\
  help='Save error at the top level (z=10 m), False if flag is absent')

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
output_data_path_root = args.output_data_path_root
fcst_nDays = args.fcst_nDays
var_names = args.var_name
forecast_file_pref = args.forecast_file_pref
nowcast_file_pref  = args.nowcast_file_pref
file_suff = args.file_suff
# --

data_date =  pd.to_datetime(proc_date)
data_date_str = data_date.strftime("%Y%m%d")

data_path = data_path_root + exp_name
data_path_today = data_path + "/" + "{}".format(data_date_str)
print("\nRead data from following path:\n{}\n".format(data_path_today))

for var in var_names:
  forecast_fNames = sorted( glob.glob(data_path_today +\
           "/" + forecast_file_pref + '*' + '_daily_3z' + var + file_suff))
  #print(forecast_fNames)

  # Read all forecast time-slices (expect 8-days) and rename time coordinate
  forecast_ds = xr.open_mfdataset(forecast_fNames).rename({'MT': 'time'})
  var_name = list(forecast_ds.keys())
  print("Differencing:\t{}".format(var_name))

  nFcst = len(forecast_ds.time)
  if nFcst < fcst_nDays:
    sys.exit("Forecast on\t{} went out to {}-days.\nSkip this date.\n\n".format(data_date_str, nFcst))

  nowcast_fNames = []
  for iDay in range(nFcst):
    next_day = forecast_ds.time[iDay]
    next_day_str = next_day.dt.strftime("%Y%m%d").values
    data_path_nowcast = data_path + "/" + next_day_str
    nowcast_fName = data_path_nowcast +\
                   "/" + nowcast_file_pref + '_daily_3z' + var + file_suff
    nowcast_fNames.append(nowcast_fName)
  #print(nowcast_fNames)
  if not all(list(map(os.path.isfile,nowcast_fNames))):
    sys.exit("\n\nNot all nowcast files needed to calculate forecast error for 8-days exist. Exiting.\n\n")

  # Read corresponding nowcasts
  nowcast_ds = xr.open_mfdataset(nowcast_fNames).rename({'MT':'time'})

  # Calculate forecast error= forecast - nowcast
  fcst_err = forecast_ds-nowcast_ds
  glb_mean = fcst_err[var_name].mean( ('Y', 'X'))

  # Save output file(s)
  fName_fcst_err_pref = output_data_path_root + '{}/'.format(exp_name) + data_date_str
  if (save_top_level):
    fcst_err.isel(Depth=0).to_netcdf( fName_fcst_err_pref +'_top_lev_fcst_err_'+ var + '.nc')
  
  # set `HDF5_USE_FILE_LOCKING=FALSE` to speed up following?
  glb_mean.to_netcdf( fName_fcst_err_pref +'_glob_mean_fcst_err_'+ var + '.nc')
