IGRA Scraper
============

Integrated Global Radiosonde Archive:
http://www.ncdc.noaa.gov/oa/climate/igra/

## Run the code

Generate a `.dat` file in `output/` directory:

```
dat.py
```

Generate the corresponding `.inv` file:

```
inv.py
```

The default command (above) extracts records for the nominal *surface*
level (identified with 9999 in the data files).  The curious can
extract data for any level:

```
dat.py --level 1000 temp_00z.mly
```
