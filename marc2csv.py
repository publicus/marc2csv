# Simple marc2csv script.

import csv
import sys

from pymarc import MARCReader

filepath = '/home/jacoblevernier/Downloads/BooksAll.2014.part01.marc8/BooksAll.2014.part01.marc8'
if len(sys.argv) > 1:
    filepath = sys.argv[1]

try:
    reader = MARCReader(open(filepath, mode="rb"), to_unicode=True,),   # Per https://groups.google.com/forum/#!topic/pymarc/GtJ7jhP7OGI, "In Python 3, you need to open the file in 'rb' mode, since MARC is a binary format and the Python 3 open() with 'r' mode would do decoding to unicode (called "str" in py3) objects."
except IOError:
    print('cannot open "%s"' % filepath, file=sys.stderr)
    sys.exit(1)

csv_records = []
marc_tags = []

for marc_record in reader:
    # Per https://groups.google.com/forum/#!topic/pymarc/Gued5iyupC0, if you see a warning like "couldn't find 0x6d in g0=52 g1=69", "What you're seeing isn't really an error....Basically, it's a warning that it couldn't translate the MARC8 character properly. Most often this sort of thing is seen when a MARC8 record contains characters from another encoding like Latin-1."
    csv_record = {}
    for marc_field in marc_record.fields:
        if marc_field.tag not in marc_tags:
            marc_tags.append(marc_field.tag)
        csv_record[marc_field.tag] = marc_field.value().strip()
    csv_records.append(csv_record)

marc_tags.sort()

print(','.join(['"%s"' % tag for tag in marc_tags]))
writer = csv.DictWriter(sys.stdout, fieldnames=marc_tags, lineterminator='\n', quotechar='"', quoting=csv.QUOTE_ALL)
writer.writerows(csv_records)
