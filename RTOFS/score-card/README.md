# Structure of files/folder(s) and order of work:

1. `data-prep`: fetch data. 
    If the data is from RTOFS production run(s), it will involve getting data from the [hpss](https://docs.rdhpcs.noaa.gov/data/nescc_hpss.html#nescc-hpss-data-structure). At the minimum, one has to fetch 2 kinds of files:
    - nowcast:
    - forecast:

2. `compute`: calculate the difference between forecast and nowcast fields.
    For now we will consider:
    - Global
    - Tropics

3. `plot`:

