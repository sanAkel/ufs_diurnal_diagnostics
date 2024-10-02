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

