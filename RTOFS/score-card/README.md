# What is being calculating?

On any day, RTOFS production (or parallel) system, 
for e.g., `20250101` generates following files:
```
> hsi ls /NCEPPROD/1year/hpssprod/runhistory/rh2025/202501/20250101/*rtofs*

/NCEPPROD/1year/hpssprod/runhistory/rh2025/202501/20250101/com_rtofs_v2.4_rtofs.20250101.grb2.tar
/NCEPPROD/1year/hpssprod/runhistory/rh2025/202501/20250101/com_rtofs_v2.4_rtofs.20250101.grb2.tar.idx
/NCEPPROD/1year/hpssprod/runhistory/rh2025/202501/20250101/com_rtofs_v2.4_rtofs.20250101.nc.tar
/NCEPPROD/1year/hpssprod/runhistory/rh2025/202501/20250101/com_rtofs_v2.4_rtofs.20250101.nc.tar.idx
```

From the `nc` formatted tar file:
```
htar -tvf /NCEPPROD/1year/hpssprod/runhistory/rh2025/202501/20250101/com_rtofs_v2.4_rtofs.20250101.nc.tar
```
Look for:
 - Nowcast files for: salinity (`s`), temperature (`t`) and currents (`u` and `v`):
```
> htar -tvf /NCEPPROD/1year/hpssprod/runhistory/rh2025/202501/20250101/com_rtofs_v2.4_rtofs.20250101.nc.tar | grep 'rtofs_glo_3dz_n024_daily_'

HTAR: -rw-rw-r--  ops.prod/prod  626100788 2025-01-01 03:18  ./rtofs_glo_3dz_n024_daily_3zsio.nc
HTAR: -rw-rw-r--  ops.prod/prod  825730270 2025-01-01 03:18  ./rtofs_glo_3dz_n024_daily_3ztio.nc
HTAR: -rw-rw-r--  ops.prod/prod  903387769 2025-01-01 03:18  ./rtofs_glo_3dz_n024_daily_3zuio.nc
HTAR: -rw-rw-r--  ops.prod/prod  905853600 2025-01-01 03:18  ./rtofs_glo_3dz_n024_daily_3zvio.nc
```

 - Forecast files for salinity, others are similar:
```
> htar -tvf /NCEPPROD/1year/hpssprod/runhistory/rh2025/202501/20250101/com_rtofs_v2.4_rtofs.20250101.nc.tar | grep 'rtofs_glo_3
dz_f' | grep '_daily_3zs'

HTAR: -rw-rw-r--  ops.prod/prod  625856016 2025-01-01 09:15  ./rtofs_glo_3dz_f024_daily_3zsio.nc
HTAR: -rw-rw-r--  ops.prod/prod  625665602 2025-01-01 09:15  ./rtofs_glo_3dz_f048_daily_3zsio.nc
HTAR: -rw-rw-r--  ops.prod/prod  625475960 2025-01-01 09:16  ./rtofs_glo_3dz_f072_daily_3zsio.nc
HTAR: -rw-rw-r--  ops.prod/prod  625319099 2025-01-01 09:16  ./rtofs_glo_3dz_f096_daily_3zsio.nc
HTAR: -rw-rw-r--  ops.prod/prod  625153554 2025-01-01 15:12  ./rtofs_glo_3dz_f120_daily_3zsio.nc
HTAR: -rw-rw-r--  ops.prod/prod  624992866 2025-01-01 15:12  ./rtofs_glo_3dz_f144_daily_3zsio.nc
HTAR: -rw-rw-r--  ops.prod/prod  624829367 2025-01-01 15:12  ./rtofs_glo_3dz_f168_daily_3zsio.nc
HTAR: -rw-rw-r--  ops.prod/prod  624670093 2025-01-01 15:12  ./rtofs_glo_3dz_f192_daily_3zsio.nc
```

## We calculate the difference between the above forecast - corresponding day's nowcast

# How is it done? 

Similar to the above date, i.e., `20250101`, we can get RTOFS nowcast for following
```
Day number:                           1     2     3     4     5     6     7     8
Nowcast days:               20250101  0102  0103  0104  0105  0106  0107  0108  0108
Forecasts from 20250101 HR:           024   048   072   096   120   144   168   192
```
In `compute/forecast_error_day.py`, for any day (say, `20250101`), we read the time-stamp in forecast files,
**find the file name** of the nowcast (see above) and difference them:

$ e_x(k) = x_f(k) - x_a(k) $

where $x$ denotes one of the following fields: salinity, temperature, zonal, meridional current (s, t, u, v).

$e_x$ denotes the forecast_error, $x_f$ and $x_n$ denote the corresponding forecast and nowcast fields, 
and $k = 1, 2, ..., 8$ denotes the day of the forecast. 

**Note**: Above files are saved at `00UTC` of any day.

# Structure of files/folder(s) and order of work:

1. `data-prep`: fetch data. 
    If the data is from RTOFS production run(s), it will involve getting data from the [hpss](https://docs.rdhpcs.noaa.gov/data/nescc_hpss.html#nescc-hpss-data-structure). At the minimum, one has to fetch 2 kinds of files:
    - Nowcast.
    - Forecast.
    - Usage: `get_files.py -h`. An example yaml has been provided and known to work (for me!).

2. `compute`: calculate the difference between forecast and nowcast fields.
    For now we will consider differences on following scales/regions (more will be added later):
    - Global.
    - Usage: 
      - `./drive_fcst_err.py -h` An example yaml has been provided and known to work (for me!).
      - `forecast_error_day.py -h` to calculate for a single day and variable, 
         above driver simply calls this over a range of dates and variables set via yaml file.

3. `plot`:

