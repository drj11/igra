#!/usr/bin/env python3

import os
import sys
import urllib.request

URL = "http://www1.ncdc.noaa.gov/pub/data/igra/igra-stations.txt"

def igra_inv(inv):
    for station in igra_stations():
        inv.write(format_single(station))

def format_single(station):
    id = "IGR{}500".format(station['wmo_id'])
    latitude = station['latitude']
    longitude = station['longitude']
    stelev = station['elevation']
    name = station['name']

    formatted = "{} {:8.4f} {:9.4f} {:6.1f} {:30.30s}".format(
      id, latitude, longitude, stelev, name)

    assert len(formatted) == 68
    return "{:107s}\n".format(formatted)

def igra_stations():
    """
    Yield a sequence of dicts, each dict representing the
    metadata for a single IGRA station. Each station is
    identified by its WMO identifier, stored as a 5 character
    string in the *wmo_id* key.
    """

    def from_url():
        f = urllib.request.urlopen(URL)
        for row in f:
            yield row.decode('ascii')
    # For checkability the columns specified here use the
    # inclusive 1-based system; same as
    # http://www1.ncdc.noaa.gov/pub/data/igra/readme.txt
    fields = dict(
      fips_country=(1, 2, str),
      wmo_id=(5, 9, str),
      name=(12, 46, str),
      latitude=(48, 53, float),
      longitude=(55, 61, float),
      elevation=(63, 66, float),
      guan=(68, 68, str),
      lks=(69, 69, str),
      composite=(70, 70, str),
      first_year=(73, 76, int),
      last_year=(78, 81, int)
      )
    for row in from_url():
        d = dict()
        for field, (b, e, convert) in fields.items():
            d[field] = convert(row[b-1:e])
        yield d

def choose_output():
    import glob
    dats = glob.glob(os.path.join("output", "*.dat"))
    if dats:
        dat = sorted(dats)[-1]
        return "{}inv".format(dat[:-3])
    else:
        return os.path.join("output", "igra.inv")

def main(argv=None):
    if argv is None:
        argv = sys.argv
    output_name = choose_output()
    with open(output_name, 'w') as inv:
        igra_inv(inv)

if __name__ == '__main__':
    main()
