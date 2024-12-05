#!/usr/bin/env python3
 
import xarray as xr
import numpy as np
import glob as glob
import cartopy.crs as ccrs
 
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
# --

NY_max = 2450 # cut off at about 60N
nSkip = 50
# Adjust the length and width of the arrows based on intensity
scale_factor = 0.05  # Adjust this factor to control the arrow size
# Define a slice to skip drawing some of the quiver arrows to reduce clutter
skip = (slice(None, None, nSkip), slice(None, None, nSkip))
# --

def cut_out_Arctic_scaled_fields(ds, NY_max):
  ds_cut = ds.sel(Y=slice(1, NY_max))
  speed = np.sqrt( ds_cut.u_velocity**2+ds_cut.v_velocity**2)
  u_scaled = ds_cut.u_velocity.squeeze() * scale_factor
  v_scaled = ds_cut.v_velocity.squeeze() * scale_factor
  return ds_cut, speed, u_scaled, v_scaled
# --
 
data_path = "/home/Santha.Akella/marineda-scratch2/data/rtofs-v2.5/" + "output/"

# List of output files
fNames = sorted( glob.glob(data_path + "time_averaged_velocity_fcst_*_day.nc"))

for iF, fName in enumerate(fNames):
  [ds, speed, u, v]= cut_out_Arctic_scaled_fields( xr.open_dataset(fName), NY_max)

  fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': ccrs.PlateCarree()})
  im = ax.pcolormesh(speed.Longitude, speed.Latitude, speed.squeeze(), cmap='Blues', vmin=0., vmax=1.)

  # Use the quiver function to display current vectors with their direction and intensity
  ax.quiver(speed.Longitude[skip], speed.Latitude[skip], u[skip], v[skip],\
            color='black', scale=2, width=0.003, headwidth=4)

  ax.coastlines()

  # Add a color scale for ocean current intensity
  cbar = plt.colorbar(im, ax=ax, orientation='horizontal', pad=0.01,shrink=1.0)
  cbar.set_label('Diff (para-prod) current speed day: {} [m/s]'.format(str(iF).zfill(2)))

  figName = data_path + "mean_velocity_at_00UTC_day_{}.png".format( str(iF).zfill(2))
  plt.savefig(figName, dpi=120)
  plt.close('all')
  print("Saved plot to:\n{}".format(figName))
