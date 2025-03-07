#!/usr/bin/env python3

import xarray as xr

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

ic_restarts = "gdas.201912*/18/model/ocean/restart/*.000000.MOM.res.nc"
dPath_hr5 = "/scratch1/NCEPDEV/climate/role.ufscpara/IC/HR5/C1152mx025/20250110/"
output_path = "/scratch1/NCEPDEV/stmp2/Santha.Akella/data/HR5/data_prepared/"

ds = xr.open_mfdataset(dPath_hr5+ic_restarts, decode_times=False)
rst_sst = ds.Temp.isel(Layer=1)

rst_sst.to_netcdf(output_path + 'ic_sst_201912.nc')
