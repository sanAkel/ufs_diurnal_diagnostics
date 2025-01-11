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
# --

# user inputs

get_inputs = argparse.ArgumentParser(prog='\nplot_av_full_depth.py',\
          description='To plot and compare mean of forecast errors for full depth', usage='%(prog)s [options]')

get_inputs.add_argument('--input_data_path_root', type=str,\
          help='path where forecast error files were saved',\
          default='/collab1/data/Santha.Akella/RTOFS/score_card/fcst_err/')

get_inputs.add_argument('--output_data_path', type=str,\
          help='path where plots are to be saved',\
          default='/collab1/data/Santha.Akella/RTOFS/score_card/fcst_err/plots/')

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

get_inputs.add_argument('--depth_cutOff', type=float,\
          help='Plot between 0- [THIS depth]', default=1250.)

get_inputs.add_argument('--num_exp', type=int,\
          help='Number of experiment(s) from which to read data', default=2)

args = get_inputs.parse_args()
# --

data_path_root = args.input_data_path_root
output_data_path = args.output_data_path
var_name = args.var_name
date_s, date_e = [args.start_date, args.end_date]

# Following are set for RTOFS
fPref = "AV_glob_mean_fcst_err_"

Z0 = args.depth_cutOff # plot depth: 0- Z0

if args.num_exp > 1:
  exp_names= ["v2.4", "v2.5"]
  do_comparison= True
# --

fig=plt.figure( figsize=(12, 4), dpi=180)
ax=fig.add_subplot(111)

for iexp, exp_name in enumerate(exp_names):
  fName = data_path_root + "{}/{}_".format(exp_name, exp_name) +\
          fPref + var_name +\
          "_{}_{}.nc".format(date_s, date_e)

  if os.path.exists( fName):
    #print("Reading data from:\n{}".format(fName))
    ds = xr.open_dataset(fName)
  else:
    print("Processed file:\n{}\ndoes not exist. Fix and try again!".format(fName))

  nSamples = int(ds[var_names[var_name]].attrs['num_samples'])
  print("Exp name:\t{}, has {} forecast samples.".format(exp_name, nSamples))
  if (args.num_exp > 1) and (iexp==0): # save the first (experiment) dataset for comparison with others.
    ds_ctl = ds
    nSamples_ctl = nSamples

  fig=plt.figure( figsize=(10, 6), dpi=180)
  ax=fig.add_subplot(111)
  ds[var_names[var_name]].sel(Depth=slice(0, Z0)).plot(yincrease=False)

  figName= output_data_path + '{}_full_depth_mean_err'.format(exp_name) +\
           '_'+var_name+'_'+args.start_date+'_'+args.end_date+'.png'
  plt.savefig(figName, bbox_inches='tight')
  print("Saved plot to:\n{}".format(figName))
  plt.close()

  if (iexp>0) and (do_comparison):
    fig=plt.figure( figsize=(10, 6), dpi=180)
    ax=fig.add_subplot(111)
    (ds[var_names[var_name]]-ds_ctl[var_names[var_name]]).sel(Depth=slice(0, Z0)).plot(yincrease=False)
    ax.set_title("{}({}) - {}({})".format(exp_name, nSamples, exp_names[0], nSamples_ctl))

    figName= output_data_path + 'diff_{}_minus_{}_full_depth_mean_err'.format(exp_name, exp_names[0]) +\
             '_'+var_name+'_'+args.start_date+'_'+args.end_date+'.png'
    plt.savefig(figName, bbox_inches='tight')
    print("Saved difference plot to:\n{}".format(figName))
    plt.close()
