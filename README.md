# What can this code do?
Ocean (and surface) oriented diurnal diagnostics with the ufs-weather-model output.

# What's needed for it to work?
- Access to:
  - ufs-weather-model output (of course)!
  - If the output is on [RDHPCS](https://docs.rdhpcs.noaa.gov/), then access to the system(s).
    - Here we assume _you_ have access to [NESCC HPSS](https://docs.rdhpcs.noaa.gov/data/nescc_hpss.html), if not, see above and request access to it.
  - A _decent_ python environment. To make our life simpler, see below example.

# Python enviroment/packages.
Following instructions are for [RDHPCS-hera](https://docs.rdhpcs.noaa.gov/systems/hera_user_guide.html) 

If these do not suffice _your_ needs, 
either [read and follow these instructions](https://docs.rdhpcs.noaa.gov/software/python/index.html) or 
figure it out; good luck!

```
module use /contrib/miniconda3/modulefiles/
ml miniconda3/4.12.0
#conda env list
conda activate /scratch2/NCEPDEV/marineda/Santha.Akella/envs/py31013
```


