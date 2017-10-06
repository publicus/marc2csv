marc2csv
========

marc2csv - command-line tool to convert a MARC file to an Excel-ready CSV file.

Overview
--------

This is a very simple command-line tool built for Unix-like (POSIX) systems.
Potentially runs on Windows, but is only tested on GNU/Linux.
Requires Python and pymarc.

http://pypi.python.org/pypi/pymarc

A batch script for GNU bash is also included.

Usage
-----

    python marc2csv.py path/to/data.mrc

Where path/to/data.mrc is the marc file you'd like to convert.  CSV is printed
to stdout.  To create a CSV file, simply:

    python marc2csv.py path/to/data.mrc > data.csv

If you have multiple MARC files to convert, you can either use the included
marc2csv_batch bash script, or concatenate all of your MARC files into one,
i.e.

    cat data1.mrc data2.mrc data3.mrc > data.mrc
    python marc2csv.py data.mrc > data.csv

If you see warning messages such as this:

    couldn't find 0x29 in g0=52 g1=69

Per a [Google Group discussion](https://groups.google.com/forum/#!topic/pymarc/Gued5iyupC0), this output (which comes from the `pymarc` library, is "basically ... a warning that it couldn't translate the MARC8 character properly. Most often this sort of thing is seen when a MARC8 record contains characters from another encoding like Latin-1." In these cases, the output CSV should still be correct.

Output CSV
----------

The output CSV is a spreadsheet which has a column for each MARC tag found in
the input data.  If a marc record does not have the tag, the corresponding cell
is empty.  If you want one CSV for multiple marc files, the easiest approach is
to concatenate all marc files into one before generating the CSV.  (Otherwise
the columns will not likely line up in the output CSV files.)  You can open
this CSV with OpenOffice or Microsoft Excel.

For more on MARC, see http://www.oclc.org/bibformats/en/default.shtm

License & Copyright
-------------------

Freely available under the GNU General Public License (GPL) v3.  See COPYING.

Copyright (C) the following contributors (listed in reverse chronological order):

- (2017) Jacob Levernier
- (2010) The Associated Universities, Inc. Washington DC, USA.
