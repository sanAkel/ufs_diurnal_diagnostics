#!/usr/bin/env python3

import xarray as xr
import glob as glob

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

data_path = "/home/Santha.Akella/marineda-scratch2/data/rtofs-v2.5/" + "output/"
vName="speed"

# List of output files
fNames_mean = sorted( glob.glob(data_path + "*_mean_{}".format(vName) + ".nc"))
fNames_sdev = sorted( glob.glob(data_path + "*_sdev_{}".format(vName) + ".nc"))

#print(fNames_mean)
#print(fNames_sdev)

#ds_sdev = xr.open_mfdataset( fNames_sdev)

fig, ax = plt.subplots( figsize=(12, 8), nrows=2, ncols=1, sharex=True, clear=True)

# plot mean
for iF, fName in enumerate(fNames_mean):
  #print(iF, fName)
  ds= xr.open_dataset( fName)
  ds.speed.plot( ax=ax[0])

# plot sdev
for iF, fName in enumerate(fNames_sdev):
  #print(iF, fName)
  ds= xr.open_dataset( fName)
  ds.speed.plot( ax=ax[1])

ax[0].set_xlabel('')
ax[1].set_xlabel('Time')

ax[0].set_ylabel('Mean [m/s]')
ax[1].set_ylabel('Std dev [m/s]')

ax[0].set_title('Diff current speed: Parallel (v2.5) - Production (v2.4) ')
ax[1].set_title('')

figName = data_path + "global_mean_sdev_" + vName + ".png"
plt.savefig(figName, dpi=120)
plt.close('all')

print("Saved plot to:\n{}".format(figName))
