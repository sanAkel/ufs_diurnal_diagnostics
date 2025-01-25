#!/usr/bin/env python3

import argparse
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
        "t": "temperature"}

var_units = {
        "s": "[PSU]",
        "t": "[deg C]"}

# ## Inputs
get_inputs = argparse.ArgumentParser(prog='\nplot_diff_error-stats.py',\
                  description='To plot RTOFS forecast error difference in mean and RMSE', usage='%(prog)s [options]')

data_path_root = '/collab1/data/Santha.Akella/RTOFS/score_card/fcst_err/'
output_data_path = data_path_root + '/plots/'
exp_names = ['v2.4', 'v2.5']
get_inputs.add_argument('--var_name', type=str,\
                  help='Variable name, one of: s, t', required=True)

start_date = pd.to_datetime('2024-11-15')
end_date = pd.to_datetime('2024-12-24')

args = get_inputs.parse_args()
# --

var_name = args.var_name
fSuff = '{}_{}_{}.nc'.format(var_name, start_date.strftime('%Y%m%d'), end_date.strftime('%Y%m%d'))

# ## Read precomputed mean and std dev of forecast errors

for iexp, exp_name in enumerate(exp_names):
    
    input_data_path = data_path_root + exp_name + '/'
    fName_mean = input_data_path + '3d_' + 'mean_' + fSuff
    fName_sdev = input_data_path + '3d_' + 'sdev_' + fSuff
    print(f'\nReading:\nMean error: {fName_mean}\nStd dev error: {fName_sdev}')

    ds_mean_exp = xr.open_dataset(fName_mean)
    ds_sdev_exp = xr.open_dataset(fName_sdev)
    if iexp ==0:
        ds_mean_ctl = ds_mean_exp
        ds_sdev_ctl = ds_sdev_exp

# ## Plot diff in global mean and standard deviation

for z0 in ds_mean_ctl.Depth.values:
  if z0 < 1500.:

    (np.abs(ds_mean_exp[var_names[var_name]])-np.abs(ds_mean_ctl[var_names[var_name]])).\
    sel(Depth=z0, method='nearest').plot(x="X", y="Y", col="time", col_wrap=4,\
    vmin=-0.5, vmax=0.5, cmap="bwr")
    figName1=output_data_path + 'diff_mean_{}_{}_minus_{}_at_{}m.png'.format(var_name, exp_names[1], exp_names[0], str(z0)) 
    plt.savefig(figName1, bbox_inches='tight')
    plt.close('all')

    (ds_sdev_exp[var_names[var_name]]-ds_sdev_ctl[var_names[var_name]]).\
    sel(Depth=z0, method='nearest').plot(x="X", y="Y", col="time", col_wrap=4,\
    vmin=-1.0, vmax=1., cmap="bwr")
    figName2=output_data_path + 'diff_rmse_{}_{}_minus_{}_at_{}m.png'.format(var_name, exp_names[1], exp_names[0], str(z0)) 
    plt.savefig(figName2, bbox_inches='tight')
    plt.close('all')

    print(f'\nSaved figures to:\n{figName1, figName2}')
