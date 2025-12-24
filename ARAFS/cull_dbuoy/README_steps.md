# Steps to: cull out drifter buoy data from prepbufr

## Get prepbufr files. Two options:
1.a Get them from wcoss, see [README_prepbufr.md](https://github.com/sanAkel/ufs_diurnal_diagnostics/blob/main/ARAFS/cull_dbuoy/README_prepbufr.md#path-to-prepbufr-files)
1.b From [nomads server](https://nomads.ncep.noaa.gov/pub/data/nccf/com/obsproc/prod/gdas.20251223/) 
    which has only the most _recent_ data.

## Build NCEPLIBS-bufr, see [these for instructions.](https://github.com/sanAkel/ufs_diurnal_diagnostics/blob/main/ARAFS/cull_dbuoy/README_prepbufr.md#try-following-anyway-we-do-not-need-all-of-the-above)
**Note**: Load cmake module, for example: `ml cmake/3.30.2` before building.

## Make sure you can correctly identify and extract the specific (drifter buoy) type.
- Use `extract_type.sh`.
All works well, find text files like the following:
```
-rw-r--r-- 1 Santha.Akella rstprod 324M Dec 24 04:26 data/no_dbuoy/20251222/00z/drifting_buoys_raw.txt
-rw-r--r-- 1 Santha.Akella rstprod 327M Dec 24 04:27 data/no_dbuoy/20251222/06z/drifting_buoys_raw.txt
-rw-r--r-- 1 Santha.Akella rstprod 328M Dec 24 04:29 data/no_dbuoy/20251222/12z/drifting_buoys_raw.txt
-rw-r--r-- 1 Santha.Akella rstprod 326M Dec 24 04:30 data/no_dbuoy/20251222/18z/drifting_buoys_raw.txt
```

## Extract locations of the buoys to a csv file
- Use `extract_coordinates.sh`
All works well, find similar to following:
```
[Santha.Akella@ufe03 cull_dbuoy]$ ls -alh *.csv
-rw-r--r-- 1 Santha.Akella rstprod 152K Dec 24 04:46 drifting_buoys_20251222_00z.csv
-rw-r--r-- 1 Santha.Akella rstprod 152K Dec 24 04:46 drifting_buoys_20251222_06z.csv
-rw-r--r-- 1 Santha.Akella rstprod 153K Dec 24 04:46 drifting_buoys_20251222_12z.csv
-rw-r--r-- 1 Santha.Akella rstprod 163K Dec 24 04:46 drifting_buoys_20251222_18z.csv
```

## Make a plot to verify
- Use `plot_locations.py`
All works well, find
```
-rw-r--r-- 1 Santha.Akella rstprod 370K Dec 24 05:02 drifting_buoy_panels_20251222.png
```

## Finish by extracting buoys out of the prepbufr and saving a new version of prepbuf
