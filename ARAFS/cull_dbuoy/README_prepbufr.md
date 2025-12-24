# Notes on working with prepbufr/drifting buoys

## Path to prepbufr files:
**Note**:
Prepbufr files (global: gfs and gdas) for the last couple of years are in the following path.

```
santha.akella@dlogin01:~> ls -alh /lfs/h2/emc/global/noscrub/emc.global/dump/gdas.2025*/00/atmos/gdas.t00z.prepbufr | tail -n2
-rw-r----- 1 emc.global rstprod 103M Dec 22 06:01 /lfs/h2/emc/global/noscrub/emc.global/dump/gdas.20251222/00/atmos/gdas.t00z.prepbufr
-rw-r----- 1 emc.global rstprod 105M Dec 23 06:01 /lfs/h2/emc/global/noscrub/emc.global/dump/gdas.20251223/00/atmos/gdas.t00z.prepbufr
santha.akella@dlogin01:~> 
santha.akella@dlogin01:~> 
santha.akella@dlogin01:~> ls -alh /lfs/h2/emc/global/noscrub/emc.global/dump/gdas.20251*/06/atmos/gdas.t06z.prepbufr | tail -n2
-rw-r----- 1 emc.global rstprod 85M Dec 22 11:59 /lfs/h2/emc/global/noscrub/emc.global/dump/gdas.20251222/06/atmos/gdas.t06z.prepbufr
-rw-r----- 1 emc.global rstprod 89M Dec 23 11:59 /lfs/h2/emc/global/noscrub/emc.global/dump/gdas.20251223/06/atmos/gdas.t06z.prepbufr
santha.akella@dlogin01:~> 
santha.akella@dlogin01:~> ls -alh /lfs/h2/emc/global/noscrub/emc.global/dump/gdas.20251*/12/atmos/gdas.t12z.prepbufr | tail -n2
-rw-r----- 1 emc.global rstprod  87M Dec 22 18:00 /lfs/h2/emc/global/noscrub/emc.global/dump/gdas.20251222/12/atmos/gdas.t12z.prepbufr
-rw-r----- 1 emc.global rstprod  91M Dec 23 18:00 /lfs/h2/emc/global/noscrub/emc.global/dump/gdas.20251223/12/atmos/gdas.t12z.prepbufr
santha.akella@dlogin01:~> 
santha.akella@dlogin01:~> ls -alh /lfs/h2/emc/global/noscrub/emc.global/dump/gdas.20251*/18/atmos/gdas.t18z.prepbufr | tail -n2
-rw-r----- 1 emc.global rstprod  98M Dec 22 00:02 /lfs/h2/emc/global/noscrub/emc.global/dump/gdas.20251221/18/atmos/gdas.t18z.prepbufr
-rw-r----- 1 emc.global rstprod  96M Dec 23 00:01 /lfs/h2/emc/global/noscrub/emc.global/dump/gdas.20251222/18/atmos/gdas.t18z.prepbufr
```

# Tried building following so we can get bufr utilities
 - Did not get what I needed!
```
git clone git@github.com:NOAA-EMC/global-workflow.git

cd global-workflow
git submodule update --init --recursive --jobs 8
cd sorc
./build_all.sh
```

# Try following? Anyway we do NOT need all of the above!
```
git clone git@github.com:NOAA-EMC/NCEPLIBS-bufr.git
```
Follow these [build instructions.](https://github.com/NOAA-EMC/NCEPLIBS-bufr/tree/8d3227a308f43597f93f632bce1ad8dc0969c7b2#how-to-build-and-install)

```
bufr_path="/lfs/h2/emc/stmp/santha.akella/test/"

cmake -S NCEPLIBS-bufr -B NCEPLIBS-bufr/build -DCMAKE_INSTALL_PREFIX=$bufr_path/install -DMASTER_TABLE_DIR=$bufr_path/table
cmake --build NCEPLIBS-bufr/build -j4
ctest --test-dir NCEPLIBS-bufr/build
cmake --install NCEPLIBS-bufr/build
```

## Get a handle on `SFCSHP`- that is the type we want to key in on for ocean surface
Tabulate different types: `./install/bin/binv data/gdas.t18z.prepbufr.nr`
You should see something similar:
```
type        messages       subsets          bytes
 
ADPUPA            21           102         949540        4.86
AIRCFT            23          2450         219332      106.52
SATWND           289        190093       14082488      657.76
PROFLR             1             1            286        1.00
VADWND           798          2426        6590250        3.04
ADPSFC          1530        169373       15203758      110.70
SFCSHP           412         54237        4092242      131.64
RASSDA             2           170          79090       85.00
ASCATW           298        243251       14854414      816.28
SYNDAT             1            38           5146       38.00
TOTAL           3375        662141       56076546
```

- Split it by type: `install/bin/split_by_subset SFCSHP`will give 
  one file per above type, one of them will be: `SFCSHP`.

- Scan this file: `install/bin/debufr SFCSHP` will yield: `SFCSHP.debufr.out`

- Look for `T29`: 
```
grep 'T29' SFCSHP.debufr.out  | head -n10

santha.akella@dlogin09:~/my_stmp/test> grep 'T29' SFCSHP.debufr.out  | head -n10
055008  T29                          522  CODE TABLE                    DATA DUMP REPORT TYPE                           
055008  T29                          522  CODE TABLE                    DATA DUMP REPORT TYPE                           
055008  T29                          522  CODE TABLE                    DATA DUMP REPORT TYPE                           
055008  T29                          522  CODE TABLE                    DATA DUMP REPORT TYPE                           
055008  T29                          522  CODE TABLE                    DATA DUMP REPORT TYPE                           
055008  T29                          522  CODE TABLE                    DATA DUMP REPORT TYPE                           
055008  T29                          522  CODE TABLE                    DATA DUMP REPORT TYPE                           
055008  T29                          522  CODE TABLE                    DATA DUMP REPORT TYPE                           
055008  T29                          522  CODE TABLE                    DATA DUMP REPORT TYPE                           
055008  T29                          522  CODE TABLE                    DATA DUMP REPORT TYPE  
```

## What is this `522`?
- [They are: Ship with name (TAC)](https://github.com/NOAA-EMC/NCEPLIBS-bufr/blob/8d3227a308f43597f93f632bce1ad8dc0969c7b2/tables/bufrtab.CodeFlag_LOC_0_7_1#L4456)

Use data from [nomads](https://nomads.ncep.noaa.gov/pub/data/nccf/com/obsproc/prod/gdas.20251222/) since I can not read data from `prod/` (above path).

- gdas.20251222/ Gather using `binv`, for example: `binv data/gdas.t00z.prepbufr.nr | grep 'SFCSHP'`

```
Hour  messages       subsets          bytes  ??
00z   409         53830        4067300      131.61
06z   412         53988        4092568      131.04
12z   413         54196        4106248      131.23
18z   412         54237        4092242      131.64
```

- Which of the above are from [drifting buoy?](https://github.com/NOAA-EMC/NCEPLIBS-bufr/blob/8d3227a308f43597f93f632bce1ad8dc0969c7b2/tables/bufrtab.CodeFlag_LOC_0_7_1#L4468-L4470)
  
```
562 > | Fixed or drifting buoy arriving in WMO TAC FM-18 format
563 > | Fixed buoy arriving in WMO BUFR format
564 > | Drifting buoy arriving in WMO BUFR format
```

- Scan for `562`, `563` and `564`: `readbp -n  SFCSHP | grep 'TYPE' | grep '180' | grep -c '562'`
```
562 | 30
563 | 4853
564 | 4662
```

- Do the split-by-type and extract `564` using `extract_type.sh` script.
