# Steps to: cull out drifter buoy data from prepbufr

## Get prepbufr files. Two options:

1.a Get them from wcoss, see [README_prepbufr.md](https://github.com/sanAkel/ufs_diurnal_diagnostics/blob/main/ARAFS/cull_dbuoy/README_prepbufr.md#path-to-prepbufr-files)

1.b From [nomads server](https://nomads.ncep.noaa.gov/pub/data/nccf/com/obsproc/prod/gdas.20251223/) 
    which has only the most _recent_ data.

## Build NCEPLIBS-bufr, see [these for instructions.](https://github.com/sanAkel/ufs_diurnal_diagnostics/blob/main/ARAFS/cull_dbuoy/README_prepbufr.md#try-following-anyway-we-do-not-need-all-of-the-above)
**Note**: Load cmake module, for example: `ml cmake/3.30.2` on [Ursa](https://docs.rdhpcs.noaa.gov/systems/ursa_user_guide.html) before building.

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
[This figure is displayed here.](https://github.com/sanAkel/ufs_diurnal_diagnostics/issues/1#issuecomment-3689242395)

## Finish by extracting buoys out of the prepbufr and save a new version of prepbuf
- It performs a surgical extraction of NCEP Prepbufr data. 
- To remove Drifting Buoys (Report Type 564).
- While preserving Ship observations (Report Type 522) and all other atmospheric data.

### Why this logic is "Ugly" (Room to Improve)
The complexity of this script is a direct result of ??

1. **Mnemonic Fragility**: The library lacks a unified metadata abstraction.
   We are forced to check both `TYP` and `T29` mnemonics because NCEP Prepbufr 
   versions are inconsistent in how they label "Report Type."
2. **Buffering Conflict**: `BUFRLIB` cannot natively mix 
   message-level copying (`COPYMG`) and subset-level writing (`WRITSB`) 
   without explicit manual flushing (`CLOSMG`). 
   Failure to manage this leads to silent file corruption.
3. **Metadata Decoupling**: Tools like `binv` report subset counts 
   based on Section 3 headers (the "Index"), which often do not reflect 
   the actual payload in Section 4 after surgery. 
   This tool relies on internal counters for truth, not library utilities.
4. **Mixed Categories**: 
   - Drifting Buoys are frequently "misplaced" in `ADPSFC` messages 
   - Instead of `SFCSHP`. 
   - This tool forces a full inspection of both categories to ensure the 564 count "squares" with spatial plots.

## Usage
1. Compile: `gfortran prepbufr_no_dbuoy.F90 -o no_dbuoy.x $BUFRLIB_PATH`; see [example here.](https://github.com/sanAkel/ufs_diurnal_diagnostics/blob/51bc8b439e9dc77b0b3b9f72507d2028b90971cc/ARAFS/cull_dbuoy/compile.sh#L8)
2. Run: `./no_dbuoy.x <input_prepbufr> <output_prepbufr>`
3. Wrapper script: `./process_and_verify.sh` that does the culling.

# Tried a py version, see below for details.
- Use `./prepbufr_no_dbuoy.py -h` without arguments will echo usage information:

```
usage: prepbufr_no_dbuoy.py [-h] --date DATE [--code CODE] [--base_dir BASE_DIR]

Filter BUFR, count subsets, and track file sizes.

options:
  -h, --help           show this help message and exit
  --date DATE          Date to process (YYYYMMDD)
  --code CODE          The dataSubCategory to extract (1 for SFCSHP)
  --base_dir BASE_DIR  Root directory for files
```

- Example usage: `./prepbufr_no_dbuoy.py --date 20251222` 
- **Note**: `CODE` and `BASE_DIR` have defaults; provide inputs for them as needed.
- All goes well, see output similar to the following:

```
[Santha.Akella@ufe03 cull_dbuoy]$ ./prepbufr_no_dbuoy.py --date 20251222
--- Scan Started: Date=20251222 | Target SubCat=1 ---

[Cycle 00z]
  ADPSFC   | Reports: 165320 | Extracted: 3     | Kept: 165317 | Size: 14.19 MB
  ADPUPA   | Reports: 1187   | Extracted: 6     | Kept: 1181 | Size: 7.08 MB
  AIRCFT   | Reports: 2071   | Extracted: 3     | Kept: 2068 | Size: 0.22 MB
  ASCATW   | Reports: 228657 | Extracted: 3     | Kept: 228654 | Size: 13.37 MB
  RASSDA   | Reports: 156    | Extracted: 3     | Kept: 153 | Size: 0.11 MB
  SATWND   | Reports: 205043 | Extracted: 3     | Kept: 205040 | Size: 14.54 MB
  SFCSHP   | Reports: 53833  | Extracted: 3     | Kept: 53830 | Size: 3.93 MB
  SYNDAT   | Reports: 29     | Extracted: 3     | Kept: 26 | Size: 0.05 MB
  VADWND   | Reports: 1965   | Extracted: 3     | Kept: 1962 | Size: 4.96 MB
  Summary 00z: Reports=658261 | Ext=30 | Master=658231
  Sizes 00z:   Orig=58.44 MB | Ext=0.43 MB | Master=57.99 MB
```

## Remarks:
- I used the `eccodes` and a `py` utility - this was/is my preferred route than a Fortran utility.
- But it never worked; see above counts: `SFCSHP   | Reports: 53833  | Extracted: 3     | Kept: 53830 | Size: 3.93 MB`
  - They need to change by thousands!
- Pay attention to:
  Table A mnemonic (e.g., NC001001 for ships, NC001003 for drifting buoys).
