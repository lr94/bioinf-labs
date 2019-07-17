#!/bin/python3
################################################################################
# Politecnico di Torino, 2018 / 2019                                           #
# Bioinformatics (prof. Elisa Ficarra)                                         #
# Lab 3                                                                        #
# Assignment 2.1                                                               #
#                                                                              #
# Luca Robbiano, 244033                                                        #
#                                                                              #
# This program filters a gtf file extracting informations about chromosomes 10 #
# and 18, with feature = 'gene' and gene_biotype = 'protein_coding'            #
################################################################################

import sys
import re

def main():
    gft_input_file = sys.argv[1]
    gft_output_file = sys.argv[2]
    r_splitter = re.compile(r'\s*;?\s+')

    kept = counter = 0

    with open(gft_input_file, 'r') as fi, open(gft_output_file, 'w+') as fo:
        for raw_line in fi:
            if not raw_line.startswith('#!'):
                counter = counter + 1
                # Parse line
                fields = r_splitter.split(raw_line)
                chromosome = fields[0].replace('chr', '')
                feature = fields[2]
                gene_biotype = trim(fields[1 + fields.index('gene_biotype')])
                if (chromosome == '10' or chromosome == '18') and\
                        feature == 'gene' and gene_biotype == 'protein_coding':
                    kept = kept + 1
                    fo.write(raw_line)
            else:
                fo.write(raw_line)

        print("Kept %d / %d reads" % (kept, counter))


def trim(string):
    # Remove initial and final white spaces
    white = (' ', '\n', '\r', '\t')
    i = 0
    while string[i] in white:
        i = i + 1
    string = string[i:]

    i = -1
    while string[i] in white:
        i = i - 1
    if i != -1:
        string = string[0:i + 1]

    # Remove trailing ";" if present
    if string[-1] == ';':
        string = string[:-1]
    # Remove quotes
    if string[0] == '"' and string[-1] == '"':
        string = string[1:-1]

    return string


if __name__ == '__main__':
    main()
