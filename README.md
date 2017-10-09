# marc2csv

`marc2csv` - A command-line tool to convert a MARC file to a CSV file. Now for Python3 and with command-line arguments! 

## Overview

This is a simple command-line tool built for Unix-like (POSIX) systems.
It potentially runs on Windows (for example, with [Git BASH](https://git-for-windows.github.io/)), but has only been tested using Linux.

It requires the following: 

- Python3 (tested with Python 3.6.1)
- Python's [pymarc](http://pypi.python.org/pypi/pymarc) library
- Python's [argparse](https://pypi.python.org/pypi/argparse) library (may come pre-installed with Python)

An example batch script for the Bash command-line is also included.

## Usage

    python marc2csv.py path/to/data.mrc

Where path/to/data.mrc is the marc file you'd like to convert.
You can see the full help documentation output, with a full list of options, using the `--help` flag, like this:

    python marc2csv.py path/to/data.mrc --help

```
usage: marc2csv.py [-h] [-a] [-n MAX_NUMBER_OF_RECORDS_TO_PROCESS] [-l]
                   [-o OUTPUT_FILE] [--subfields-as-separate-columns]
                   [-s SUBFIELD_SEPARATOR] [--suppress-header-row] [-v]
                   filepath

Convert MARC records into CSV.

positional arguments:
  filepath              The MARC file to process.

optional arguments:
  -h, --help            show this help message and exit
  -a, --append-to-output-file
                        If set, an output file defined using the "--output-
                        file" argument will be appended to, instead of
                        overwritten.
  -n MAX_NUMBER_OF_RECORDS_TO_PROCESS, --max-number-of-records-to-process MAX_NUMBER_OF_RECORDS_TO_PROCESS
                        The maximum number of records that should be
                        processed. This can be useful for debugging or
                        otherwise exploring a dataset. Default: (Infinite)
  -l, --output-long-data
                        Write a "long" (vs. "wide" dataset). The "long"
                        dataset has three columns:
                        "random_unique_record_identifier" (a randomly-created
                        identifier for the record, to link all of the output
                        rows that belong to it), "marc_field" (the MARC field;
                        or, if "--subfields-as-separate-columns" is turned on,
                        the MARC field and subfield), and "value" (the value
                        of that MARC field).
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The file to save output to. Default: stdout (i.e., the
                        console output)
  --subfields-as-separate-columns
                        If set, columns will be broken down into MARC
                        subfields Otherwise, MARC fields will be concatenated
                        with each other, using the "subfield_separator"
                        argument.
  -s SUBFIELD_SEPARATOR, --subfield-separator SUBFIELD_SEPARATOR
                        If "--subfields-as-separate-columns" is not set, the
                        separator used when concatenating MARC subfield values
                        together. NOTE WELL that if you want subfields to be
                        separated by dashes ("-", "--", etc.), you need to use
                        the following syntax (with a "="): '--subfield-
                        separator="--"'. Default: ";"
  --suppress-header-row
                        If set, no CSV header row (put differently, no column
                        names) will be included in the output.
  -v, --verbose         Increase verbosity of output.
```

If you have multiple MARC files to convert, you can either use the included
marc2csv_batch bash script, or concatenate all of your MARC files into one,
i.e.

    cat data1.mrc data2.mrc data3.mrc > data.mrc
    python marc2csv.py data.mrc > data.csv

Or, if you know the MARC records have the same fields, you could use the `-a` / `--append-to-output-file` option, like this:

    python marc2csv.py data1.mrc --output-file example.csv
    python marc2csv.py data2.mrc --output-file example.csv --append-to-output-file --suppress-header-row

See also the `--output-long-data` option.

## Other notes:

If you see warning messages such as this:

    couldn't find 0x29 in g0=52 g1=69

Per a [Google Group discussion](https://groups.google.com/forum/#!topic/pymarc/Gued5iyupC0), this output (which comes from the `pymarc` library, is "basically ... a warning that it couldn't translate the MARC8 character properly. Most often this sort of thing is seen when a MARC8 record contains characters from another encoding like Latin-1." In these cases, the output CSV should still be correct.

## Output CSV

The output CSV is a spreadsheet which has a column for each MARC tag found in
the input data. **Each MARC subfield can be given its own column** using the `--subfields-as-separate-columns` argument; otherwise, subfields are concatenated in the same column using whatever string is given in the `--subfield-separator` arguement (**note** that if you want subfields to be separated by dashes (`-`, `--`, etc.), you need to use the following syntax: `--subfield-separator='--'`).

If a marc record does not have the tag, the corresponding cell
is empty. If you want one CSV for multiple marc files, the easiest approach is
to concatenate all marc files into one before generating the CSV. (Otherwise
the columns will not likely line up in the output CSV files.)  You can open
this CSV with OpenOffice or Microsoft Excel.

For more on MARC, see http://www.oclc.org/bibformats/en/default.shtm

# License & Copyright

`marc2csv` is released under the GNU General Public License (GPL) v3. See COPYING.

Copyright (C) the following contributors (listed in reverse chronological order):

- (2017) Jacob Levernier
- (2010) The Associated Universities, Inc. Washington DC, USA.

# News

## Version 0.1.1 (2017-10-09)

- Version number added
- `--output-long-data` option added, allowing more easily concatenating processed MARC files. This option returns a dataset that has three columns: 
    - `random_unique_record_identifier`: A randomly-created identifier for the record, to link all of the output rows that belong to it)
    - `marc_field` (the MARC field; or, if `--subfields-as-separate-columns` is turned on, the MARC field and subfield)
    - `value` (the value of that MARC field)

## (Unversioned) (2017-10-06)

- Code forked from @rduplain's [original repository](https://github.com/rduplain/marc2csv).
- Script brought up-to-date for Python 3 (tested using Python 3.6.1).
- New command-line interface built using Python's `argparse` package.