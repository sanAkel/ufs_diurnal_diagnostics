#!/usr/bin/env python3

import os
import time
import numpy as np
import glob as glob
import pandas as pd
import xarray as xr

data_path_root = "/collab1/data/Santha.Akella/RTOFS/score_card/"
exp_name = "v2.4"
proc_date = "2024-12-01"
var_name = 's'
fcst_nDays = 8
forecast_file_pref = "rtofs_glo_3dz_f"
nowcast_file_pref = "rtofs_glo_3dz_n024"
file_suff = "io.nc"

data_date =  pd.to_datetime(proc_date)
data_date_str = data_date.strftime("%Y%m%d")
data_path = data_path_root + exp_name
data_path_today = data_path + "/" + "{}".format(data_date_str)
print("\nRead data from following path:\n{}".format(data_path_today))

var = var_name
forecast_fNames = sorted( glob.glob(data_path_today + "/" + forecast_file_pref + '*' + '_daily_3z' + var + file_suff))
#print(forecast_fNames)
forecast_ds = xr.open_mfdataset(forecast_fNames, parallel=True)
forecast_ds = forecast_ds.rename({'MT': 'time'})

var_name = list(forecast_ds.keys())
nFcst = len(forecast_ds.time)

nowcast_fNames = []
for iDay in range(nFcst):
  next_day = forecast_ds.time[iDay]
  next_day_str = next_day.dt.strftime("%Y%m%d").values
  data_path_nowcast = data_path + "/" + next_day_str
  nowcast_fName = data_path_nowcast + "/" + nowcast_file_pref + '_daily_3z' + var + file_suff
  nowcast_fNames.append(nowcast_fName)
#print("\n\n")
#print(nowcast_fNames)
nowcast_ds = xr.open_mfdataset(nowcast_fNames, parallel=True)
nowcast_ds = nowcast_ds.rename({'MT':'time'})

fcst_err = forecast_ds-nowcast_ds

os.system("rm -f /collab1/data/Santha.Akella/skinSST_vs_NSST/scripts/ufs_diurnal_diagnostics/RTOFS/score-card/compute/test1.nc")
os.system("rm -f /collab1/data/Santha.Akella/skinSST_vs_NSST/scripts/ufs_diurnal_diagnostics/RTOFS/score-card/compute/test2.nc")
print("\n---------------- START --------------")
start_time = time.time()
glb_mean = fcst_err[var_name].mean( ('Y', 'X'))
glb_sdev = fcst_err[var_name].std( ('Y', 'X'))

#glb_mean.load()
#glb_mean.compute() # Preferred than `load` https://docs.xarray.dev/en/stable/user-guide/dask.html#loading-dask-arrays
                    # But `load` writes to nc FASTER! Why??
glb_mean.compute().to_netcdf('test1.nc')
glb_sdev.compute().to_netcdf('test2.nc')

end_time=time.time()
dT = end_time-start_time
print("---------------- STOP --------------\n")
print(f"\nElapsed time: {dT} seconds\n")
