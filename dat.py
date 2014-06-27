#!/usr/bin/env python3

import getopt
import gzip
import io
import itertools
import sys
import urllib.request

# See also temp_12z.mly.gz
URL = "http://www1.ncdc.noaa.gov/pub/data/igra/monthly-por/temp_00z.mly.gz"

MISSING = 9999.0

def single_level(inp, dat, level=9999):
    for station, block in itertools.groupby(single_level_years(inp, level),
      lambda t: t[0]):
        # We have WMO identifiers for all of these stations,
        # but some stations have a radiosonde station and a
        # surface air temperature station with the same WMO ID;
        # therefore we use a suffix of 500 to avoid clashing
        # with GHCN-M.
        id11 = "IGR{}500".format(station)
        ghcnm_write(id11, (t[1:] for t in block), dat)

def single_level_years(inp, selected_level):
    """
    Process the elements of the input for a single level, and yield a
    series of (wmo, year, data) triples.
    """

    def rows():
        for row in inp:
            row = row.split()
            if int(row[3]) == selected_level:
                yield row

    # Split into groups of a single year for a single station.
    for station_year, block in itertools.groupby(rows(),
      lambda r: r[:2]):
        d = [MISSING] * 12
        for row in block:
            wmo, year, month, level, temp, n = row
            # :todo: QC on n?
            d[int(month)-1] = float(temp) * 0.1
        yield wmo, year, d

def ghcnm_write(id, values, out):
    """
    `id` is the 11 character identifier.
    `values` is an iterator of (year, data) pairs.
    `out` is a writable file to which data in GHCN-M format is
    written.
    """

    def format_single(v):
        if v == MISSING:
            return "-9999   "
        # Make up a source flag of "f" for foundation.
        return "{:5.0f}  f".format(v*100)

    FORMAT = "{}{}TAVG" + ("{:8s}"*12) + "\n"
    ALL_MISSING = [MISSING]*12
    for year, data in values: 
        if data == ALL_MISSING:
            continue
        data = tuple(format_single(d) for d in data)
        formatted_row = FORMAT.format(*((id, year) + data))
        out.write(formatted_row)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    opt, arg = getopt.getopt(argv[1:], '', 'level=')
    d = dict(level=9999)
    for k,v in opt:
       if k == '--level':
           d['level'] = int(v)

    if 0:
        f = urllib.request.urlopen(URL)
        uncompressed = gzip.GzipFile(fileobj=f)
        for i, row in enumerate(uncompressed):
            row = row.decode('ascii')
            sys.stdout.write(row)
            if i >= 4:
                sys.exit()

    filename, = arg
    with open(filename) as inp:
        with open("igra-level{}.dat".format(d['level']), "w") as dat:
            single_level(inp, dat, **d)

if __name__ == '__main__':
    main()
