#!/usr/bin/env python3

import os
import argparse
import xarray as xr
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

var_names = {
        "s": "salinity",
        "t": "temperature", 
        "u": "u",
        "v": "v"}

var_units = {
        "s": "[PSU]",
        "t": "[degC]", 
        "u": "[m/s]",
        "v": "[m/s]"}
# --

# user inputs

get_inputs = argparse.ArgumentParser(prog='\nsave_mean_error.py',\
          description='To save and plot mean of global mean forecast errors', usage='%(prog)s [options]')

get_inputs.add_argument('--input_data_path_root', type=str,\
          help='path where forecast error files were saved',\
          default='/collab1/data/Santha.Akella/RTOFS/score_card/fcst_err/')

get_inputs.add_argument('--exp_name', type=str,\
          help='Variable name, one of: v2.4 or v2.5 for RTOFS', required=True)

get_inputs.add_argument('--var_name', type=str,\
          help='Variable name, one of: s, t, u, v', required=True)

get_inputs.add_argument('--start_date', type=str,\
          help='Start date for plotting',\
          metavar='example: 2024-11-15',\
          default='2024-11-15')

get_inputs.add_argument('--end_date', type=str,\
          help='End date for plotting',\
          metavar='example: 2024-12-24',\
          default='2024-12-24')

get_inputs.add_argument('--output_data_path', type=str,\
          help='path where plots are to be saved',\
          default='/collab1/data/Santha.Akella/RTOFS/score_card/fcst_err/')

args = get_inputs.parse_args()
# --

data_path_root = args.input_data_path_root
exp_name = args.exp_name
var_name = args.var_name
date_s, date_e = [args.start_date, args.end_date]
output_data_path = args.output_data_path

# Following are set for RTOFS
fPref = "_glob_mean_fcst_err_"
# --

nSamples = 0

for iDate, proc_date in enumerate(pd.date_range(pd.to_datetime(args.start_date), pd.to_datetime(args.end_date))):
  fName = data_path_root + exp_name + "/{}".format(proc_date.strftime('%Y%m%d')) + fPref + var_name + '.nc'
  if os.path.exists( fName):
    nSamples +=1
    print("Reading data from:\n{}".format(fName))
    ds = xr.open_dataset(fName)
  else:
    print("Processed file for date:\n{} does NOT exist, skipping it.".format(proc_date))

  if iDate==0:
   sum_var=np.abs( ds[var_names[var_name]].values)
  else:
   sum_var = sum_var + np.abs( ds[var_names[var_name]].values)

if nSamples > 0:
  mean_var = sum_var/nSamples

da = xr.DataArray( 
      np.transpose(mean_var),
      dims=("Depth", "time"),
      coords={"Depth": ds.Depth.values, "time": np.arange(1, ds.time.shape[0]+1)},
      attrs={"num_samples": str(nSamples), "units": var_units[var_name]})

# Save it to a file for (later) comparisons
fName_out= output_data_path + '{}/'.format(exp_name) +\
           '{}'.format(exp_name) + '_AV_' + fPref[1:-1] + '_'+var_name+'_'+args.start_date+'_'+args.end_date+'.nc'
ds_out=xr.Dataset({var_names[var_name]: da})
ds_out.to_netcdf(fName_out)
print("\n\nSaved calculated mean error to:\n{}".format(fName_out))
