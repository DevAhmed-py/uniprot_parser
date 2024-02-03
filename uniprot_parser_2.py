#!/usr/bin/env python3

### Author: Ahmed Tijani Akinfalabi
### Date: 2024-02-02
### Name: UniProt-Parser 
### Description: Parser 2

"""Uniprot-Parser by Ahmed Tijani Akinfalabi, 2024
Extract information from Uniprot data files.
-------------------------------------------
Optional arguments are:
    --help - display this help page
    --go   - show a protein id to GO id mapping
    --doi  - show a protein id to DOI mapping (not used today)

Mandatory arguments are:
    FILE - one or more compressed or uncompressed Uniprot data files \n
"""

import sys, os, gzip

class UniProtParse:
    def __init__(self):
        self.entries = []

    def help(self, argv):
        print(f"\nUsage: {argv[0]} --help|--go|--doi [FILE] ?[FILE] ...?")
        print(__doc__)

    def check_file(self, argv):
        for file in argv[2:]:
            if os.path.isfile(file):
                if argv[1] == '--go':
                    self.entries = self.get_go_ids(file)
                elif argv[1] == '--kegg':
                    self.entries = self.get_kegg_ids(file)
                elif argv[1] == '--doi':
                    self.entries = self.get_doi_ids(file)
            else:
                print(f'The file `{file}` does not exist')
            if not (file.endswith('dat.gz') or file.endswith('dat')):
                if file.find('.') != -1:
                    print(f'Error: Unknown file extension `{file.split(".")[-1]}`, known extensions are `dat.gz` or `dat`!')


    # DR   GO; GO:0020002;
    # re.compile(r'\s+GO; GO:\d+; .*')
    def get_go_ids(self, filename):
        entries = []
        current_entry_lines = []
        open_function = gzip.open if filename.endswith('.gz') else open

        with open_function(filename, 'rt') as uniprot_file:
            for line in uniprot_file:
                if line.startswith('//'):
                    entry = {'ID': None, 'GO': []}

                    for entry_line in current_entry_lines:
                        if entry_line.startswith('ID'):
                            entry['ID'] = entry_line.split()[1]                       # Index 0 is ID, Index 1 is the number
                        elif entry_line.startswith('DR') and 'GO;' in entry_line:
                            go_number = entry_line.split(';')[1].strip()
                            entry['GO'].append(go_number)

                    entries.append(entry)
                    current_entry_lines = []
                else:
                    current_entry_lines.append(line)
        return entries

    # DR   KEGG; vg:921684;
    # re.compile(r'\s+KEGG;\s+vg:\d+;')
    def get_kegg_ids(self, filename):
        entries = []
        current_entry_lines = []
        open_function = gzip.open if filename.endswith('.gz') else open

        with open_function(filename, 'rt') as uniprot_file:
            for line in uniprot_file:
                if line.startswith('//'):
                    entry = {'ID': None, 'KEGG': []}

                    for entry_line in current_entry_lines:
                        if entry_line.startswith('ID'):
                            entry['ID'] = entry_line.split()[1]                       
                        elif entry_line.startswith('DR') and 'KEGG;' in entry_line:
                            # kegg_number = entry_line.split(';')[1].strip()           # This is used to get the number as vg:921684
                            kegg_number = entry_line.split()[1:3]                      # This was used to get the number as KEGG; vg:921684;
                            kegg_number = ' '.join(kegg_number)
                            entry['KEGG'].append(kegg_number)

                    entries.append(entry)
                    current_entry_lines = []
                else:
                    current_entry_lines.append(line)
        return entries

    # RX   PubMed=33422265; DOI=10.1016/j.devcel.2020.12.010;
    # re.compile(r'DOI=(10\.\d+/\S+);')
    def get_doi_ids(self, filename):
        entries = []
        current_entry_lines = []
        open_function = gzip.open if filename.endswith('.gz') else open

        with open_function(filename, 'rt') as uniprot_file:
            for line in uniprot_file:
                if line.startswith('//'):
                    entry = {'ID': None, 'DOI': []}

                    for entry_line in current_entry_lines:
                        if entry_line.startswith('ID'):
                            entry['ID'] = entry_line.split()[1]                       
                        elif entry_line.startswith('RX') and 'DOI=' in entry_line:
                            doi_number = entry_line.split(';')[1].strip()
                            entry['DOI'].append(doi_number)

                    entries.append(entry)
                    current_entry_lines = []
                else:
                    current_entry_lines.append(line)
        return entries
    

    def main(self, argv):
        if (len(argv)) < 2 or argv[1] == "--help":  # You shouldn't use sys.argv inside a function
            self.help(argv)
            sys.exit(0)

        if not sys.argv[1] in ['--go', '--doi', '--kegg']:
            print("Wrong argument! Valid arguments are --help | --go | --doi | --kegg")
        
        if len(argv) < 3:
            print('Missing filename! Please enter a filename')
        
        else:
            self.check_file(argv)
            print(f"\nUniprot ID \t Numbers")
            print("-" * 27)
            for entry in self.entries:
                id_value = entry['ID']
                if argv[1] == '--go':
                    values = entry['GO'] if entry['GO'] else ['NA']
                elif argv[1] == '--kegg':
                    values = entry['KEGG'] if entry['KEGG'] else ['NA']
                elif argv[1] == '--doi':
                    values = entry['DOI'] if entry['DOI'] else ['NA']
                
                for value in values:
                    print(f'{id_value} \t {value}')
                    

if __name__ == "__main__":
    uniprot = UniProtParse()
    uniprot.main(sys.argv)
