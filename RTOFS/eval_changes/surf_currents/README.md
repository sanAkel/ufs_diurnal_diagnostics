# Files of following type is what Jessica uses:
`rtofs_glo_2ds_f*_prog.nc`

# To extract them from the hpss archive (for e.g., from `20241110` output):

- `Production`: 
```
htar -xvf /NCEPPROD/1year/hpssprod/runhistory/rh2024/202411/20241110/com_rtofs_v2.4_rtofs.20241110.nc.tar ./rtofs_glo_2ds_f*_prog.nc
```

- `Parallel`: 
```
htar -xvf emc-ocean/5year/Dan.Iredell/rtofs.v2.5.test01/rtofs.20241110/rtofs.ncgrb.tar rtofs_glo_2ds_f*_prog.nc
```

# Python usage:
```
module use /contrib/miniconda3/modulefiles/
ml miniconda3/4.12.0
conda activate /scratch2/NCEPDEV/marineda/Santha.Akella/envs/py31013
```

# Description of scripts:
- `get_files.py` To get files from `hpss` archive/tape system; this takes time!
- `drive_diff.py` feeds dates to `diff_surf_fields.py`, latter writes out:
   - Global mean and standard deviation of surface speed differences.
   - Differences in u- and v- velocities at 00 UTC.
- `plot_time_av_surf_speed_mean_diff.py` plots above global mean and std deviations time-series.
- `calculate_time_averaged_velocity.py` Calculates time-averaged differences in currents.
- `plot_time_averaged_velocity.py` plots above currents (quiver plot).

## Note:
These scripts assume familiarity with certain python functionality. 
While they are being provided, there should be no expectation at
_your_ end that _free_ support will be provided to make them work for _you_.

