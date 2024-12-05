#!/usr/bin/env python3

import xarray as xr
import numpy as np
import glob as glob

data_path = "/home/Santha.Akella/marineda-scratch2/data/rtofs-v2.5/" + "output/"
nDays = np.arange(0, 9)

# List of output files
fNames = sorted( glob.glob(data_path + "*_uv_vel.nc"))

# Mean for all time slices
nSamples = len(fNames)

for iDay in nDays:
  print(iDay)

  # --
  for iF, fName in enumerate(fNames):
    #print(iF, fName)
    ds= xr.open_dataset( fName) # concat will not work easily, so one-by-one.
    if iF == 0:
      mean_var = ds.isel(MT=iDay)
    else:
      mean_var = mean_var+ds.isel(MT=iDay)
  # --

  mean_var = mean_var/float(nSamples)
  fName_mean = data_path + "time_averaged_velocity_fcst_{}_day.nc".format(str(iDay).zfill(2))
  mean_var.to_netcdf(fName_mean)
  print("Saved data to:\n{}".format(fName_mean))

