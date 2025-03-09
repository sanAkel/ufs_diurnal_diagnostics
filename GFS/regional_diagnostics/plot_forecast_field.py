#!/usr/bin/env python3

import glob as glob
import numpy as np
import pandas as pd
import xarray as xr

import warnings
warnings.filterwarnings('ignore')

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import matplotlib.ticker as mticker

import cartopy.crs as ccrs
import cartopy.feature as cfeature
# --
#
# Following way to set inputs is nasty! Should be yaml-ized as in:
# https://github.com/sanAkel/ufs_diurnal_diagnostics/blob/main/RTOFS/score-card/data-prep/get_files.py
#
exp_name = "HR5-winter"
data_path = "/scratch1/NCEPDEV/stmp2/Santha.Akella/data/HR5/" +\
            "data_prepared/" + exp_name + "/"

fcst_start_date, fcst_end_date = ['2019-12-03', '2019-12-30'] # 00UTC
fcst_days_skip = "3D"

# US North East coast
lon_s, lon_e = [-79, -74]
lat_s, lat_e = [33, 41]

cLat = -180 # central longitude (map proj)

plot_skip = 4 # skip [4 \times 6 hours = 24 hours] 
vName = 'SST'
cMin, cMax, cMap = [5., 25., 'Set1_r']
fSize=8 # text font size
DPI = 180
# --

subplot_kws=dict(projection=ccrs.PlateCarree(central_longitude=cLat), facecolor='grey')

start_date, end_date = [pd.to_datetime(fcst_start_date), pd.to_datetime(fcst_end_date)]
for data_date in pd.date_range(start_date, end_date, freq=fcst_days_skip):
  fName = sorted( glob.glob(data_path+'{}*{}.nc'.format(exp_name, data_date.strftime('%Y%m%d'))))
  print(f'Reading data from:\t{fName}')

  ds = xr.open_dataset(fName[0])
  ds = ds.assign_coords({'geolon': ds['geolon'], 'geolat': ds['geolat']})
  # make time index pretty
  datetimeindex = ds.indexes['time'].to_datetimeindex()
  ds['time'] = datetimeindex
  # skip sample
  ds_sampled = ds.isel(time=slice(0, -1, plot_skip))
  time_slices_plot = ds_sampled.time
  
  # plot
  fig = plt.figure( figsize=(12, 10))
  for iT, time_plot in enumerate(time_slices_plot):
      ax = plt.subplot(4,4,iT+1, projection=ccrs.PlateCarree()) # will not be pretty!

      # Add features like coastlines, gridlines, etc.
      ax.add_feature(cfeature.LAND, facecolor='grey', alpha=0.1)
      ax.coastlines()
      ax.set_extent([lon_s, lon_e, lat_s, lat_e], crs=ccrs.PlateCarree())

      im = ds_sampled[vName].sel(time=time_plot, method="nearest").\
           plot(ax=ax, x='geolon', y='geolat', transform=ccrs.PlateCarree(),\
           add_colorbar=False, vmin=cMin, vmax=cMax, cmap=cMap)

      # Set the title
      date1 = time_plot.values
      yyyymmdd = time_plot.values.astype('str').split('T')[0]
      ax.text(lon_s, lat_e-1, "{}".format(yyyymmdd),
              zorder=15, fontsize=12,color='k', transform=ccrs.PlateCarree())
      ax.set_title('')

  # add separate colorbar
  cax = fig.add_axes([0.91, 0.15, 0.01, 0.75]) # Create an inset axes
  cb = plt.colorbar(im, cax, ticks=np.arange(cMin, cMax, (cMax-cMin)/10), shrink=0.5)
  cb.ax.tick_params(labelsize=6)
  cb.ax.set_xlabel(ds_sampled[vName].units, fontsize=12)

  plt.subplots_adjust(wspace=-0.2, hspace=-0.0)
  # save figure
  figName = data_path + '{}_{}.png'.format(vName, data_date.strftime('%Y%m%d'))
  plt.savefig(figName, dpi=DPI, bbox_inches='tight')
  print(f'Saved\t:{figName}')
  print('\n')
