# Simple marc2csv script.

import csv
import sys
from pymarc import MARCReader
import argparse
import logging
import math
import uuid

# Settings:

argument_parser = argparse.ArgumentParser(description='Convert MARC records into CSV.')

argument_parser.add_argument('filepath',
                             action='store',
                             help='The MARC file to process.')

argument_parser.add_argument('-a',
                             '--append-to-output-file',
                             action='store_true',
                             help='If set, an output file defined using the "--output-file" argument will be appended to, instead of overwritten.')

argument_parser.add_argument('-n', 
                             '--max-number-of-records-to-process',
                             action='store',
                             help='The maximum number of records that should be processed. This can be useful for debugging or otherwise exploring a dataset. Default: (Infinite)',
                             default=math.inf)

argument_parser.add_argument('-l',
                             '--output-long-data',
                             action='store_true',
                             help='Write a "long" (vs. "wide" dataset). The "long" dataset has three columns: "random_unique_record_identifier" (a randomly-created identifier for the record, to link all of the output rows that belong to it), "marc_field" (the MARC field; or, if "--subfields-as-separate-columns" is turned on, the MARC field and subfield), and "value" (the value of that MARC field).')

argument_parser.add_argument('-o',
                             '--output-file',
                             action='store',
                             help='The file to save output to. Default: stdout (i.e., the console output)')

argument_parser.add_argument('--subfields-as-separate-columns',
                             action='store_true',
                             help='If set, columns will be broken down into MARC subfields Otherwise, MARC fields will be concatenated with each other, using the "subfield_separator" argument.')

argument_parser.add_argument('-s', 
                             '--subfield-separator',
                             action='store',
                             help='If "--subfields-as-separate-columns" is not set, the separator used when concatenating MARC subfield values together. NOTE WELL that if you want subfields to be separated by dashes ("-", "--", etc.), you need to use the following syntax (with a "="): \'--subfield-separator="--"\'. Default: ";"',
                             default=';')

argument_parser.add_argument('--suppress-header-row',
                             action='store_true',
                             help='If set, no CSV header row (put differently, no column names) will be included in the output.')

argument_parser.add_argument('-v',
                             '--verbose',
                             action='store_true',
                             help='Increase verbosity of output.')

# Parse the command-line arguments:
parsed_arguments = argument_parser.parse_args()

if parsed_arguments.verbose:
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('Verbose mode is turned on.')
else:
    logging.basicConfig(level=logging.INFO) 


# An example for accessing the parsed command-line arguments:
logging.debug('Maximum number of records to process: ' + str(parsed_arguments.max_number_of_records_to_process))

try:
    reader = MARCReader(open(parsed_arguments.filepath, mode="rb"), to_unicode=True)   # Per https://groups.google.com/forum/#!topic/pymarc/GtJ7jhP7OGI, "In Python 3, you need to open the file in 'rb' mode, since MARC is a binary format and the Python 3 open() with 'r' mode would do decoding to unicode (called "str" in py3) objects."
except IOError:
    print('cannot open "%s"' % parsed_arguments.filepath, file=sys.stderr)
    sys.exit(1)

csv_records = []
marc_tags = []

if parsed_arguments.subfields_as_separate_columns:
    logging.debug('Processing each MARC subfield as a separate column...')
else:
    logging.debug('Processing each MARC subfield in the same column...')

record_number = 1

if parsed_arguments.max_number_of_records_to_process != math.inf:
    parsed_arguments.max_number_of_records_to_process = int(parsed_arguments.max_number_of_records_to_process)

for marc_record in reader:
    if record_number <= parsed_arguments.max_number_of_records_to_process:
        logging.info('Processing record number %s...' %record_number)
        
        csv_record = {}
        
        if parsed_arguments.output_long_data:
            # If we've been asked to output long-format data, we'll create a random (and thus hopefully unique) ID number for each record. We'll do this instead of using record_number in case multiple datasets get appended.
            random_unique_record_number = str(uuid.uuid4().fields[0])  # Take just the first part of a UUID string -- hopefully, that will be enough to avoid collisions.
            logging.debug('Since the "output-long-data" option is turned on, using the following random (and hopefully unique) ID for this record: "%s"' %random_unique_record_number)
            csv_record['random_unique_record_number'] = random_unique_record_number
        
        for marc_field in marc_record.get_fields():
            if parsed_arguments.subfields_as_separate_columns:
                for marc_subfield in list(marc_field):
                    marc_subfield_tag = marc_field.tag+marc_subfield[0]
                    if marc_subfield_tag not in marc_tags:
                        marc_tags.append(marc_subfield_tag)
                    csv_record[marc_subfield_tag] = marc_subfield[1].strip()
            else:
                if marc_field.tag not in marc_tags:
                    marc_tags.append(marc_field.tag)
                csv_record[marc_field.tag] = parsed_arguments.subfield_separator.join([subfield_value[1].strip() for subfield_value in list(marc_field)])
        csv_records.append(csv_record)
        
        record_number = record_number + 1
    else:
        break

marc_tags.sort()

if parsed_arguments.output_file is not None:
    # If we have a file to write to, do so:
    if parsed_arguments.append_to_output_file:
        output_file = open(parsed_arguments.output_file, mode='a')
    else:
        output_file = open(parsed_arguments.output_file, mode='w')
else:
    output_file = sys.stdout

if parsed_arguments.output_long_data:
    output_csv_field_names = ['random_unique_record_identifier',
                              'marc_field',
                              'value']
    csv_string_of_field_names = ','.join(['"%s"' % tag for tag in output_csv_field_names])
else: 
    output_csv_field_names = marc_tags
    csv_string_of_field_names = ','.join(['"%s"' % tag for tag in marc_tags])

if not parsed_arguments.suppress_header_row:
    if parsed_arguments.output_file is not None:
        output_file.write(csv_string_of_field_names)
    else:
        print(csv_string_of_field_names)
else:
    logging.debug('Not printing a header row for the output CSV...')

# logging.info('Output file is "'+parsed_arguments.output_file+'"...')    

writer = csv.DictWriter(output_file,
                        fieldnames=output_csv_field_names,
                        lineterminator='\n', 
                        quotechar='"', 
                        quoting=csv.QUOTE_ALL,
                        doublequote=False,
                        escapechar='\\')

if parsed_arguments.output_long_data:
    for csv_record in csv_records:        
        long_formatted_csv_data = {}
        
        long_formatted_csv_data['random_unique_record_identifier'] = csv_record['random_unique_record_number']
        
        for key, value in [(key, value) for key, value in csv_record.items() if key is not 'random_unique_record_number']:  # Exclude the random ID numbers, since they'll get printed using the 'random_unique_record_number' key above with each row, anyway.
            long_formatted_csv_data['marc_field'] = key
            long_formatted_csv_data['value'] = value
            
            writer.writerow(long_formatted_csv_data)
else:
    writer.writerows(csv_records)

if output_file != sys.stdout:
    output_file.close
