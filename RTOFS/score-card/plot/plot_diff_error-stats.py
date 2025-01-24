#!/usr/bin/env python3

import numpy as np
import pandas as pd
import xarray as xr
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

data_path_root = '/collab1/data/Santha.Akella/RTOFS/score_card/fcst_err/'
output_data_path = data_path_root + '/plots/'
exp_names = ['v2.4', 'v2.5']
var_name = 's' 

start_date = pd.to_datetime('2024-11-15')
end_date = pd.to_datetime('2024-12-24')

fSuff = '{}_{}_{}.nc'.format(var_name, start_date.strftime('%Y%m%d'), end_date.strftime('%Y%m%d'))


# ## Read precomputed mean and std dev of forecast errors

for iexp, exp_name in enumerate(exp_names):
    
    input_data_path = data_path_root + exp_name + '/'
    fName_mean = input_data_path + '3d_' + 'mean_' + fSuff
    print(f'Reading:\nMean error: {fName_mean}')

    ds_mean_exp = xr.open_dataset(fName_mean)
    if iexp ==0:
        ds_mean_ctl = ds_mean_exp


# ## Plot diff in global mean and standard deviation

z0=100

(np.abs(ds_mean_exp[var_names[var_name]])-np.abs(ds_mean_ctl[var_names[var_name]])).\
sel(Depth=z0, method='nearest').plot(x="X", y="Y", col="time", col_wrap=4)

plt.savefig('x1.png')

for iexp, exp_name in enumerate(exp_names):
    
    input_data_path = data_path_root + exp_name + '/'
    fName_sdev = input_data_path + '3d_' + 'sdev_' + fSuff
    print(f'Reading:\nStd dev error: {fName_sdev}')

    ds_sdev_exp = xr.open_dataset(fName_sdev)
    if iexp ==0:
        ds_sdev_ctl = ds_sdev_exp

z0=100

(ds_sdev_exp[var_names[var_name]]-ds_sdev_ctl[var_names[var_name]]).\
sel(Depth=z0, method='nearest').plot(x="X", y="Y", col="time", col_wrap=4)

plt.savefig('x2.png')
