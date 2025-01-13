#!/usr/bin/env python3

import os
import argparse
import sys
import glob as glob
import numpy as np
import pandas as pd
import xarray as xr

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

import warnings
warnings.filterwarnings('ignore')

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

get_inputs = argparse.ArgumentParser(prog='\nplot_mean_sdev_at_depth.py',\
                  description='To plot and compare global mean and std dev of forecast errors from RTOFS', usage='%(prog)s [options]')

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

output_data_path = args.output_data_path
data_path_root = args.input_data_path_root
var_name = args.var_name
Z0 = args.depth
date_s, date_e = [pd.to_datetime(args.start_date), pd.to_datetime(args.end_date)]

sigma_frac=0.1 # how many standard deviations to plot?

# Following are set for RTOFS
exp_names = ["v2.4", "v2.5"]
fPref = ["_glob_mean_fcst_err_", "_glob_sdev_fcst_err_"]
nDays = 8
# --

# ## Read forecasts from each day and plot mean/std dev from analysis

nSamples = np.zeros( len(exp_names))
mean_var = np.zeros( (nDays, len(exp_names)))
sdev_var = np.zeros_like( mean_var)

fig=plt.figure( figsize=(12, 4), dpi=180)
ax=fig.add_subplot(111)

for iDate, proc_date in enumerate(pd.date_range(date_s, date_e)):
    for iexp, exp_name in enumerate(exp_names):
        for iFile, stat_file in enumerate(fPref):
            fName = data_path_root + exp_name + "/{}".format(proc_date.strftime('%Y%m%d')) + stat_file + var_name + '.nc'
            
            if not os.path.exists( fName):
                print("Processed file:\n{} does NOT exist, skipping it.".format(fName))
                break
                
            if iFile==0: # count mean or std dev only once!  
                nSamples[iexp] +=1
                
            #print("Reading data from:\n{}".format(fName))
            ds = xr.open_dataset(fName)
            if iFile==0: # mean
                today_mean = ds.sel(Depth=Z0, method='nearest')[var_names[var_name]]
                mean_var[:, iexp] = mean_var[:,iexp]+np.abs( today_mean.values)
            else: # std dev
                today_sdev = ds.sel(Depth=Z0, method='nearest')[var_names[var_name]]
                sdev_var[:,iexp] = sdev_var[:,iexp]+ today_sdev.values
                
            # plot mean for the (two) experiments
            if iFile==0:
                if iexp==0:
                    im1 = today_mean.plot(ax=ax, c='b', ls='--', marker='o', label="{}".format(exp_name))
                else:
                    im1 = today_mean.plot(ax=ax, c='k', ls='-', lw=2, marker='x', label="{}".format(exp_name))
            else: # add std dev (shaded)
                if iexp==0:
                    ax.fill_between(ds.time, today_mean.values-sigma_frac*today_sdev.values, today_mean.values+sigma_frac*today_sdev.values, 
                                    color='b', alpha=0.1)
                else:
                    ax.fill_between(ds.time, today_mean.values-sigma_frac*today_sdev.values, today_mean.values+sigma_frac*today_sdev.values, 
                                    color='k', alpha=0.1)
                    
        if (iDate==0):
            ax.legend(loc=1)
    
for iexp, exp_name in enumerate(exp_names):
    mean_var[:, iexp]=mean_var[:,iexp]/nSamples[iexp]
    sdev_var[:, iexp]=sdev_var[:,iexp]/nSamples[iexp]

ax.axhline(y=0, ls='-', c='k', alpha=0.25)
ax.set_title("")
ax.set_ylabel("{} {} at {} m".format(var_names[var_name], var_units[var_name], Z0))

figName= output_data_path + 'depth_{}m_'.format(str(Z0)) +\
         fPref[0][1:-1] + '_'+ fPref[1][1:-1]+ '_' + var_name+'_'+\
         "{}_{}.png".format(date_s.strftime('%Y%m%d'), date_e.strftime('%Y%m%d'))
plt.savefig(figName, bbox_inches='tight')
print("Saved plot to:\n{}".format(figName))
plt.close()
# --

print("\n\nMean Absolute Error and RMSE over {} days\n\n".format(nDays))
print(exp_names)
print("mean error:")
print(mean_var)
print("std dev in error")
print(sdev_var)

fig=plt.figure( figsize=(10, 4), dpi=180)
ax=fig.add_subplot(111)
for iexp, exp_name in enumerate(exp_names):
  if iexp ==0:
    ax.errorbar(np.arange(1, nDays+1), mean_var[:,iexp], yerr=0.01*sdev_var[:,iexp], capsize=4, marker='o', ls='--',\
               label="{} ({})".format(exp_name, int(nSamples[iexp])))
  else:
    ax.errorbar(np.arange(1, nDays+1), mean_var[:,iexp], yerr=0.01*sdev_var[:,iexp], capsize=4, marker='x', ls='-',\
                label="{} ({})".format(exp_name, int(nSamples[iexp])))
      
ax.legend(loc=1)
ax.set_ylabel("{} {} at {} m".format(var_names[var_name], var_units[var_name], Z0))
ax.set_xlabel("Days")
ax.axhline(y=0, c='k', alpha=0.5)

figName= output_data_path + 'depth_{}m_AvAllDays_'.format(str(Z0)) +\
         fPref[0][1:-1] + '_'+ fPref[1][1:-1]+ '_' + var_name+'_'+\
         "{}_{}.png".format(date_s.strftime('%Y%m%d'), date_e.strftime('%Y%m%d'))
plt.savefig(figName, bbox_inches='tight')
print("Saved plot to:\n{}".format(figName))
plt.close()
