# To work with data on [hpss](https://docs.rdhpcs.noaa.gov/data/nescc_hpss.html#nescc-hpss-data-structure)

Load needed module: `ml hpss`

- List what is available:
```
hsi ls /ESRL/BMC/fim/5year/Shan.Sun/hr4hydro_20240726/c96mx100/
```

- List files in any (tar) file:
```
htar -tvf /ESRL/BMC/fim/5year/Shan.Sun/hr4hydro_20240726/c96mx100/19940501/c96mx100_atm_raw_sfcf_19940501.tar
```

- Fetch a single file:
```
htar -xvf /ESRL/BMC/fim/5year/Shan.Sun/hr4hydro_20240726/c96mx100/19940501/c96mx100_atm_raw_sfcf_19940501.tar atmos/history/gefs.t00z.sfcf0006.nc
```

- Entire archive:
```
htar -xvf /ESRL/BMC/fim/5year/Shan.Sun/hr4hydro_20240726/c96mx100/19940501/c96mx100_atm_raw_sfcf_19940501.tar
```

# Usage:
## Shell scripts:
1. `driver_get_hpss_data.csh`: is a driver script for `get_exp_data.csh`.
   **Note**: Instead of command line, I chose to manually fill in the script.
2. `get_exp_data.csh`:
    Try: `./get_exp_data.csh`, it will echo (STDOUT) expected inputs and modules.
- Above were tested on [niagara.](https://docs.rdhpcs.noaa.gov/systems/niagara_user_guide.html)

## Python scripts:
- Below were tested on [Ursa.](https://www.nextplatform.com/2024/09/06/noaa-gets-100-million-windfall-for-rhea-research-supercomputer/)
1. See [env set up](https://github.com/sanAkel/ufs_diurnal_diagnostics/blob/main/README.md#on-ursa)
