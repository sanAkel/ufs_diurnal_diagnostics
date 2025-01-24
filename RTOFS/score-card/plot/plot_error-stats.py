#!/usr/bin/env python3

import numpy as np
import pandas as pd
import xarray as xr
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
        "t": "[deg C]", 
        "u": "[m/s]",
        "v": "[m/s]"}

def plot_stat(ds, exp_name, output_path, setDepth=0, stat='mean', vName='t'):

    width, height = [10, 5]

    if stat=='mean':
        cMin, cMax, cMap, nCol = [-1., 1., "bwr", 9]
    else: # std dev
        cMin, cMax, cMap, nCol = [0., 2., "viridis", 11]
        
    ds.sel(Depth=setDepth, method='nearest')[var_names[vName]].\
    plot.contourf(x="X", y="Y", col="time", col_wrap=4, figsize=(width, height),\
                  vmin=cMin, vmax=cMax, cmap=cMap, levels=np.linspace(cMin, cMax, nCol))

    figName = output_path + '{}_{}_{}_at_{}m.png'.format(exp_name, stat, vName, str(setDepth))
    plt.savefig(figName, bbox_inches='tight')
    print("Saved plot to:\n{}".format(figName))
    plt.close()

def plot_mean_sdev_at_depth(ds_mean, ds_sdev, exp_name, output_path, setDepth=0, setTimeSlice=7, vName='t'):
    
    v1 = ds_mean.sel(Depth=setDepth, method='nearest')[var_names[vName]].isel(time=setTimeSlice).squeeze()
    v2 = ds_sdev.sel(Depth=setDepth, method='nearest')[var_names[vName]].isel(time=setTimeSlice).squeeze()
    
    fig = plt.figure( figsize=(8, 6))
    ax=fig.add_subplot(111)

    # Mean
    im1=ax.contourf(ds_mean['X'].values, ds_mean['Y'].values, v1,
               vmin=-1., vmax=1, cmap="bwr", levels=np.linspace(-1, 1, 9))
    # Std. deviation
    im2=ax.contour(ds_mean['X'].values, ds_mean['Y'].values, v2,
               levels=np.asarray([0., 0.75, 1., 2., 3]), colors=('0.2', '0.3', '0.4', '0.5', '0.6'))
    
    cbar=plt.colorbar(im1, ax=ax)
    cbar.set_label("{} error {}".format(var_names[vName], var_units[vName]))
    ax.clabel(im2, fontsize=12)

    figName = output_path + '{}_{}_at_{}m_at{}HR.png'.format(exp_name, vName, str(setDepth), setTimeSlice)
    plt.savefig(figName, bbox_inches='tight')
    print("Saved plot to:\n{}".format(figName))
    plt.close()


# ## Inputs

data_path_root = '/collab1/data/Santha.Akella/RTOFS/score_card/fcst_err/'
output_data_path = data_path_root + '/plots/'
exp_name = 'v2.5'
var_name = 's' 

start_date = pd.to_datetime('2024-11-15')
end_date = pd.to_datetime('2024-12-24')

input_data_path = data_path_root + exp_name + '/'
fSuff = '{}_{}_{}.nc'.format(var_name, start_date.strftime('%Y%m%d'), end_date.strftime('%Y%m%d'))

fName_mean = input_data_path + '3d_' + 'mean_' + fSuff
fName_sdev = input_data_path + '3d_' + 'sdev_' + fSuff
print(f'Reading:\nMean error: {fName_mean}\nStandard deviation: {fName_sdev}')


# ## Read precomputed mean and std dev of forecast errors

ds_mean = xr.open_dataset(fName_mean)
ds_sdev = xr.open_dataset(fName_sdev)

# ## Plot mean and standard deviation
# - Slices at different depths (up to 1500 m)
# - Both mean (shaded) and standard deviation (contour) at a depth.

for z0 in ds_mean.Depth.values:
    if z0 < 500.:
        print(f'Plotting at {z0} m')
        plot_stat(ds_mean, exp_name, output_data_path, z0, 'mean', var_name)
        plot_stat(ds_sdev, exp_name, output_data_path, z0, 'sdev', var_name)

# surface
z0=0
plot_mean_sdev_at_depth(ds_mean, ds_sdev, exp_name, output_data_path, z0, 0, var_name) # start time (day 1)
plot_mean_sdev_at_depth(ds_mean, ds_sdev, exp_name, output_data_path, z0, 7, var_name) # start time (day 7)

# 100 m
z0=100
plot_mean_sdev_at_depth(ds_mean, ds_sdev, exp_name, output_data_path, z0, 0, var_name) # start time (day 1)
plot_mean_sdev_at_depth(ds_mean, ds_sdev, exp_name, output_data_path, z0, 7, var_name) # start time (day 7)
