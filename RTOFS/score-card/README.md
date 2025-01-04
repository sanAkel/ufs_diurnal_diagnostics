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

