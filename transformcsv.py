# merge-csv.py - Merge multiple CSVs with the same column structure, fail
#                gracefully when CSVs don't match
# Author: Tim Ubbens, 2016-11
import argparse
import logging
import sys
import glob

# CONFIGURATION:
log_format = '%(asctime)s - %(levelname)s - %(message)s'
log_date_format = '%Y/%m/%d %H:%M:%S'
log_level = logging.INFO

# throw_system_exit_code = true will cause this script to exit with the code
# specified in system_exit_code if headers in the CSV files don't match
throw_system_exit_code = True
system_exit_code = 1

# PROCESSING:
#  - receives any number of input CSV files as command line args (named or wildcard)
#  - receives an optional output CSV file as command line arg (otherwise uses default)
#  - optionally checks that header rows of the CSV files match before trying to merge
#    (will fail if they don't match)
#  - uses the header row of the first file as the header for the output file
#  - merges the contents of CSV files only when the header of the CSV matches the header
#    of the output CSV (same as header of first input CSV)
#  - writes warnings for each file that was skipped due to header mismatch
#  - optionally throws a system exit code when any warnings were raised (useful for
#    passing error codes back to a calling script or application)

def main():
    parser = argparse.ArgumentParser(description='Select and transform PiHealth CSV file...')
    parser.add_argument('file', nargs='*', help='csv files to be merged')
    parser.add_argument('--output', default='PiHealth_stripped.csv', help='output file to write to')
    parser.add_argument('--wildcard', help='a wildcard selection of files to include ex: --wildcard=test*.csv')
    parser.add_argument('--checkheadersfirst', help='check that all file headers are the same before allowing a merge to happen', action='store_true')
    # parser.set_defaults(checkheadersfirst=False)
    

    args = parser.parse_args()

    logging.basicConfig(format=log_format, datefmt=log_date_format, level=log_level)
    logging.info('======= Starting File Merge =======')

    # check for a command line argument
    if args.file:
        input_files = args.file
    elif args.wildcard is not None:
        input_files = glob.glob(args.wildcard)
    else:
        killmerge('NO INPUT FILES SPECIFIED')

    # check that output file is not included in input file list
    if args.output in input_files:
        killmerge('OUTPUT FILE INCLUDED IN INPUT FILES')

    #if args.checkheadersfirst:
    #    logging.info('Checking headers on files')
    #    if merge(input_files, args.output, args.checkheadersfirst) > 0:
    #        killmerge('HEADERS IN FILES DO NOT MATCH')

    # call merge with input and output
    merge(input_files, args.output)

    logging.info('Filenames ' + ', '.join(input_files))
    logging.info('Output: ' + args.output)
    file_errors = merge(input_files, args.output, False)
    logging.info('======= Finished File Merge =======')
    logging.warning('======= NUM FILES SKIPPED AS ERRORS: ' + str(file_errors) + ' =======')

    if throw_system_exit_code == True and file_errors > 0:
        killmerge('MERGE COMPLETED WITH WARNINGS')


#def merge(input_files, output_file, checkheaders):
merge(input_files, output_file):
    # input_files is a list of all files to be processed
    # output_file is the output file to write to
    # checkheaders is true/false - true if this function should only check
    #    the headers & not perform the merge
    # returns the number of files with headers that do not match
    first_header = ''
    num_file_error_headers = 0
    with open(output_file,'wb') as file_out:
        for filename in input_files:
            with open(filename) as file_in:
                logging.debug('Filename: ' + filename)
                header = next(file_in)
                logging.debug('Header: ' + header)
                # if this is the first file, the header will be blank
                if first_header == '':
                    first_header = header
                    if not checkheaders:
                        file_out.write(header)
                    logging.debug('Output Header: ' + first_header)
                # check that the header of each successive file is the same
                # as the first file
                # if it is, write the contents of the file to the output
                # if it isn't, log an error
                if header != first_header:
                    # skip this file because the header is different
                    logging.warning('File ' + filename + ' has a different header and will be skipped')
                    num_file_error_headers += 1
                    continue
                if not checkheaders:
                    logging.debug(filename + ' contents:')
                    for line in file_in:
                        logging.debug(line)
                        file_out.write(line)
    return num_file_error_headers


def killmerge(error_string):
    logging.warning('======= ' + error_string + ' =======')
    logging.warning('======= EXITING WITH WARNING =======')
    sys.exit(system_exit_code)


def __init__():
    return

if __name__ == '__main__':
    main()
