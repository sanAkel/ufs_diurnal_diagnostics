#!/usr/bin/env python3

import os
import sys
import glob as glob
import numpy as np
import pandas as pd
import xarray as xr

def check_files_exist(fNames):
  if not all(list(map(os.path.isfile, fNames))):
    sys.exit("\n\nExpected files are not present in path. Exiting.\n\n")

def rename_RTOFS_time(ds, new_name="time"):
  ds = ds.rename({'MT':new_name})
  return ds

def get_forecast_error( proc_date, data_path, exp_name, \
  forecast_file_pref, nowcast_file_pref, var, file_suff, fcst_nDays=8):

  data_date =  pd.to_datetime(proc_date)
  data_date_str = data_date.strftime("%Y%m%d")

  data_path = data_path + exp_name
  data_path_today = data_path + "/" + "{}".format(data_date_str)
  print("\nRead data from following path:\n{}\n".format(data_path_today))

  forecast_fNames = sorted( glob.glob(data_path_today +\
           "/" + forecast_file_pref + '*' + '_daily_3z' + var + file_suff))
  #print(forecast_fNames)

  # Read all forecast time-slices (expect 8-days) and rename time coordinate
  forecast_ds = xr.open_mfdataset(forecast_fNames, parallel=True, engine="h5netcdf")
  #with xr.open_mfdataset( forecast_fNames) as forecast_ds:
  #  forecast_ds.load()
  forecast_ds = rename_RTOFS_time(forecast_ds)

  var_name = list(forecast_ds.keys())
  #print("Differencing:\t{}".format(var_name))

  nFcst = len(forecast_ds.time)
  if nFcst < fcst_nDays:
    sys.exit("Forecast on\t{} went out to {}-days.\nSkip this date.\n\n".format(data_date_str, nFcst)) 

  nowcast_fNames = []
  for iDay in range(nFcst):
    next_day = forecast_ds.time[iDay]
    next_day_str = next_day.dt.strftime("%Y%m%d").values
    data_path_nowcast = data_path + "/" + next_day_str
    nowcast_fName = data_path_nowcast +\
                   "/" + nowcast_file_pref + '_daily_3z' + var + file_suff
    nowcast_fNames.append(nowcast_fName)
  #print(nowcast_fNames)
  check_files_exist(nowcast_fNames)

  # Read corresponding nowcasts
  nowcast_ds = xr.open_mfdataset(nowcast_fNames, parallel=True, engine="h5netcdf")
  #with xr.open_mfdataset( nowcast_fNames) as nowcast_ds:
  #  nowcast_ds.load()
  nowcast_ds = rename_RTOFS_time(nowcast_ds)

  # Calculate forecast error= forecast - nowcast
  fcst_err = forecast_ds-nowcast_ds

  # For aggregation, we need to drop 'Date', lat and lon aren't useless too
  fcst_err = fcst_err.drop_vars(["Date", "Longitude", "Latitude"])
  fcst_err = fcst_err.assign_coords(time=np.arange(1, fcst_nDays+1))

  return forecast_fNames, nowcast_fNames, fcst_err
