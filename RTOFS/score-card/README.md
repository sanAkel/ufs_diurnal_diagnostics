# What is being used in calculations?

Following gives an example of which files are being used.
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

It is clear from the :arrow_up: example that for any given day ($d$), we have:

- A nowcast, denote that by $x_n(d),$
- Forecast fields: $x_f(d+k).,$
- Where $k$ denotes 1, 2, 3, ..., 8 days, all these forecasts and nowcasts are saved at `00` UTC.
- Where $x$ denotes one of the following fields: salinity, temperature, zonal, meridional current, in short: `s`, `t`, `u`, `v`.

For $d$=`20250101`, we can get following RTOFS forecasts:

```
Day number (k):                         1     2     3     4     5     6     7     8
Nowcast days(d):              20250101  0102  0103  0104  0105  0106  0107  0108  0108
Forecast HOUR from 20250101:            024   048   072   096   120   144   168   192
```

Given nowcasts (or analyses) and forecasts valid on any given day, we can calculate forecast error (in hindcast mode),
$e_x(k) = x_f(k) - x_n(k),$ for $k= 1, 2, ...8; x= [s, t, u, v],$ as if the analysis is _truth_. 
Such calculation is possible only if we have saved the analysis fields ($x_n$) for the 8 days that 
correspond to the days of the forecast ($x_f$).  

Each $e_x(k)$ is a 3-d field of dimensions: $[n_i, n_j, n_k]$ where the horizontal and vertical resolutions are denoted 
by $n_i \times n_j$ and $n_k$ respectively.

- We calculate spatial statistics: global mean ($\mu$) and standard deviation (sdev; $\sigma$) of any $e_x(k).$
- Therefore, for each $k,$ we have $\mu(k)$ and $\sigma(k)$ at each of the vertical depth levels: $n_k.$
  - In `compute/forecast_error_day.py`, for any day (say, $d=$ `20250101`), we read the time-stamp ($k$) in forecast files,
**find the file name** of the nowcast (see above) and difference them to calculate: $e(k)$ :arrow_right: $\mu(k), \sigma(k)$ for any variable ($x$).
  - In `compute/save_mean_error.py`, we calculate the mean and standard deviation over all days ($d$) or `number of samples`. 
- Another useful metric is to calculate the day-1, day-2, ..., day-8 forecast errors at any depth level ($n_k$).
  For this, we aggregate all forecasts from different initialization dates ($d$): $e_d(k)$ to calculate mean:
  $\frac{1}{N_d}\sum e_d(k)$ for each $k=1, 2, ..., 8$ and similarly standard deviation.
  - **Note**: The sample size for this calculaion is the number of available hindcasts: $N_d.$
  - In `??.py` ...







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
      - `./save_mean_error.py -h` Calculate and save the absolute (global) mean averaged error for the `8`-days of forecast, average is based on ALL forecasts.

3. `plot`:
    - `./plot_glb_mean_at_depth.py -h` Plot Global mean error for all days of forecast and averaged for `8` days (i.e., 2 plots) for an input depth.
    - `./plot_av_full_depth.py -h` Plot averages from ALL forecasts, calculated using `compute/save_mean_error.py`
