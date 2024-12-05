#!/usr/bin/env python3

import xarray as xr
import numpy as np
import argparse

import warnings
warnings.filterwarnings("ignore")

# user inputs
data_path = "/home/Santha.Akella/marineda-scratch2/data/rtofs-v2.5/"
#proc_date = "20241110"
utc_hour = 0 # UTC hour at which we _monitor_ difference
vName = 'speed'
# --

# user inputs
get_inputs = argparse.ArgumentParser(prog='\ndiff_surf_fields.py',\
        description='Calculate and save difference between 2 RTOFS forecasts.', usage='%(prog)s [options]')

get_inputs.add_argument('--date', type=str,\
                                metavar='date in yyyymmdd format (str)', required=True)
args = get_inputs.parse_args()
# --

proc_date = args.date
print(proc_date)
ds1 = xr.open_mfdataset(data_path + "v2.4/" + proc_date + "/" +"rtofs_glo_2ds_f*_prog.nc")
ds2 = xr.open_mfdataset(data_path + "v2.5/" + proc_date + "/" +"rtofs_glo_2ds_f*_prog.nc")

# add speed to the dataset(s)- eases our life!
ds1['speed'] = xr.DataArray(np.sqrt(ds1.u_velocity**2 + ds1.v_velocity**2),\
               coords=ds1.u_velocity.coords, dims=ds1.u_velocity.dims, name='speed', attrs={'units':'m/s'})
ds2['speed'] = xr.DataArray(np.sqrt(ds2.u_velocity**2 + ds2.v_velocity**2),\
               coords=ds2.u_velocity.coords, dims=ds2.u_velocity.dims, name='speed', attrs={'units':'m/s'})

# difference
du = ds2-ds1

du_hr = du.where( du.MT.dt.hour==0, drop=True)
# care to _monitor_ difference in velocity only (for now).
du_hr = du_hr[['u_velocity', 'v_velocity']]

# time-series of difference: mean and standard deviation
mean_diff = du[vName].mean(dim=["X","Y"], skipna=True)
sdev_diff = du[vName].std(dim=["X","Y"], skipna=True)

# save output
output_path = data_path + "output/"
fName_vel = output_path + proc_date + "_uv_vel.nc"
du_hr.to_netcdf(fName_vel)
print("Saved u- and v-velocities to:\n{}".format(fName_vel))
#
fName_mean = output_path + proc_date + "_mean_{}".format(vName) + ".nc"
fName_sdev = output_path + proc_date + "_sdev_{}".format(vName) + ".nc"
mean_diff.to_netcdf(fName_mean)
sdev_diff.to_netcdf(fName_sdev)

print("Saved:\n{}\n{}".format(fName_mean, fName_sdev))
