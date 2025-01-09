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

get_inputs = argparse.ArgumentParser(prog='\nplot_glb_mean_at_depth.py',\
          description='To plot and compare global mean forecast errors from RTOFS', usage='%(prog)s [options]')

get_inputs.add_argument('--input_data_path_root', type=str,\
          help='path where forecast error files were saved',\
          default='/collab1/data/Santha.Akella/RTOFS/score_card/fcst_err/')

get_inputs.add_argument('--output_data_path', type=str,\
          help='path where plots are to be saved',\
          default='/collab1/data/Santha.Akella/RTOFS/score_card/fcst_err/plots/')

get_inputs.add_argument('--var_name', type=str,\
          help='Variable name, one of: s, t, u, v', required=True)

get_inputs.add_argument('--depth', type=float,\
          help='Depth (nearest) in m', required=True)

get_inputs.add_argument('--start_date', type=str,\
          help='Start date for plotting',\
          metavar='example: 2024-11-15',\
          default='2024-11-15')

get_inputs.add_argument('--end_date', type=str,\
          help='End date for plotting',\
          metavar='example: 2024-12-24',\
          default='2024-12-24')

args = get_inputs.parse_args()
# --

output_data_path = args.output_data_path #"/collab1/data/Santha.Akella/RTOFS/score_card/fcst_err/plots/"
data_path_root = args.input_data_path_root #"/collab1/data/Santha.Akella/RTOFS/score_card/fcst_err/"
var_name = args.var_name #'s'
Z0 = args.depth #0

date_s, date_e = [args.start_date, args.end_date] #['20241115', '20241224']
exp_names = ["v2.4", "v2.5"]
fPref = "_glob_mean_fcst_err_"
nDays = 8
# --

nSamples = np.zeros( len(exp_names))
mean_var = np.zeros( (nDays, len(exp_names)))

fig=plt.figure( figsize=(12, 4), dpi=180)
ax=fig.add_subplot(111)

for iDate, proc_date in enumerate(pd.date_range(pd.to_datetime(args.start_date), pd.to_datetime(args.end_date))):
    for iexp, exp_name in enumerate(exp_names):
      fName = data_path_root + exp_name + "/{}".format(proc_date.strftime('%Y%m%d')) + fPref + var_name + '.nc'
      if os.path.exists( fName):
        nSamples[iexp] +=1
        print("Reading data from:\n{}".format(fName))
        ds = xr.open_dataset(fName)
        mean_var[:, iexp] = mean_var[:,iexp]+np.abs( ds.sel(Depth=Z0, method='nearest')[var_names[var_name]].values)
      else:
        print("Processed file for date:\n{} does NOT exist, skipping it.".format(proc_date))

      if iexp ==0:
        im1 = ds.sel(Depth=Z0, method='nearest')[var_names[var_name]].plot(c='b', ls='-', marker='o', label="{}".format(exp_name))
      else:
        im1 = ds.sel(Depth=Z0, method='nearest')[var_names[var_name]].plot(c='b', ls='--', marker='x', label="{}".format(exp_name))

      if (iDate==0):
        ax.legend(loc=1)
    
for iexp, exp_name in enumerate(exp_names):
    mean_var[:, iexp]=mean_var[:,iexp]/nSamples[iexp]

ax.axhline(y=0, ls='-', c='k', alpha=0.5)
ax.set_title("")
ax.set_ylabel("{} {}".format(var_names[var_name], var_units[var_name]))

figName= output_data_path + 'depth_{}m_'.format(str(Z0)) + fPref[1:-1] + '_'+var_name+'_'+args.start_date+'_'+args.end_date+'.png'
plt.savefig(figName)
print("Saved plot to:\n{}".format(figName))
plt.close()
# --

print("\n\nMean Absolute Error over {} days\n\n".format(nDays))
print(exp_names)
print(mean_var)

fig=plt.figure( figsize=(10, 4), dpi=180)
ax=fig.add_subplot(111)
for iexp, exp_name in enumerate(exp_names):
  if iexp ==0:
    ax.plot( np.arange(1, nDays+1), mean_var[:, iexp], c='b', ls='-', marker='o', label="{}".format(exp_name))
  else:
    ax.plot( np.arange(1, nDays+1), mean_var[:, iexp], c='b', ls='--', marker='x', label="{}".format(exp_name))
ax.legend(loc=1)
ax.set_ylabel("{} {}".format(var_names[var_name], var_units[var_name]))
ax.set_xlabel("Days")

figName= output_data_path + 'depth_{}m_AvAllDays_'.format(str(Z0)) + fPref[1:-1] + '_'+var_name+'_'+args.start_date+'_'+args.end_date+'.png'
plt.savefig(figName)
print("Saved plot to:\n{}".format(figName))
plt.close()
