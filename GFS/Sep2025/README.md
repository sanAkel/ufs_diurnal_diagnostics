# List of experiments listed in [GFS17 Ocean and Sea Ice weekly meeting notes](https://docs.google.com/document/d/1BHeuqmgqUnIB0R6OOKOflc9ITJBAtZNYn5L2xPAAixE/edit?usp=sharing) on 09/22/2025:

1. MOM6 Edits C384mx025 (C384mx025_3DVarAOWCDA)
   - B1: everything is based on Jessica's `rt14` branch
   - `/NCEPDEV/emc-global/1year/Jiande.Wang/GAEAC6/scratch/B1`
   - Finished **1 month run**
2. B2: replace MOM6 with the latest code and bug-free MOM_input
   - `/NCEPDEV/emc-global/1year/Jiande.Wang/GAEAC6/scratch/B2`
   - Only 1 day of run remaining
3. B3: same as B2 but adding Santha's parameter tuning.
   - `/NCEPDEV/emc-global/1year/Jiande.Wang/GAEAC6/scratch/B3`
   - 5 day of run remaining

# Jiande copied `ocean` output to Ursa:
`/scratch3/NCEPDEV/climate/Jiande.Wang/working/scratch/C384-v17/OCEAN/{expName}/`
where `{expName}` = B1, B2, B3.

## Details:
- Data in above path (on Ursa):
  - Starting date: `20250101`. 
  - End date varies:
    - `B1`: 20250101 - 20250201: 32 days.
    - `B2`: 20250101 - 20250130: 30 days.
    - `B3`: 20250101 - 20250126: 26 days.
  - On start date, starting hour: `06`.

# Analysis/Plots:
- See path to figures: `/home/Santha.Akella/for_folks/JiandeW/Sep2025/figs/`
1. 20250101T06: Plot top level potential temperature and salinity (SST and SSS respectively) and compare with WOA.
2. 20250126T00: Same as above. Was chosen because it is last dataset available for all experiments.
 
