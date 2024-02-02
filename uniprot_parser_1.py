#!/usr/bin/env python3

### Author: Ahmed Tijani Akinfalabi
### Date: 2024-02-02
### Name: UniProt-Parser 
### Description: Parser 1

import sys, os

def help(argv):
    print(f"\nUsage: {argv[0]} --help|--go|--doi [FILE] ?[FILE] ...?")
    print("""Uniprot-Parser by Ahmed Tijani Akinfalabi, 2024
Extract information from Uniprot data files.
-------------------------------------------
Optional arguments are:
    --help - display this help page
    --go   - show a protein id to GO id mapping
    --doi  - show a protein id to DOI mapping (not used today)
Mandatory arguments are:
    FILE - one or more compressed or uncompressed Uniprot data files \n
          """)

def check_file(argv):
    for file in argv[2:]:
        if os.path.isfile(file):
            if argv[1] == '--go':
                go()
            else:
                doi()
        else:
            print(f'The file `{file}` does not exist')
        if not (file.endswith('dat.gz') or file.endswith('dat')):
            if file.find('.') != -1:
                print(f'Error: Unknown file extension `{file.split(".")[-1]}`, known extensions are `dat.gz` or `dat`!')

def go():
    print("Let's GO!")

def doi():
    print("Let's DO this!")

def main(argv):
    if (len(argv)) < 2 or argv[1] == "--help":  # You shouldn't use sys.argv inside a function
        help(argv)
        sys.exit(0)

    if not sys.argv[1] in ['--go', '--doi']:
        print("Wrong argument! Valid arguments are --help|--go|--doi")
    
    if len(argv) < 3:
        print('Missing filename! Please enter a filename')
    
    else:
        if argv[1] == '--go':
            check_file(argv)

        elif argv[1] == '--doi':
            check_file(argv)

if __name__ == "__main__":
    main(sys.argv)  