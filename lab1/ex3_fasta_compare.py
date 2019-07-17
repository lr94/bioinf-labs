#!/bin/python3
################################################################################
# Politecnico di Torino, 2018 / 2019                                           #
# Bioinformatics (prof. Elisa Ficarra)                                         #
# Lab 1                                                                        #
# Assignment 3                                                                 #
#                                                                              #
# Luca Robbiano, 244033                                                        #
#                                                                              #
# This program compares two fasta files and stores the result in a third fasta #
# file. The output file will contain only the common reads. Example:           #
# ./ex3_fasta_compare.py a.fa b.fa out.fa                                      #
################################################################################

import sys


def trim(string):
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

    return string


def main():
    input_file1 = sys.argv[1]
    input_file2 = sys.argv[2]
    output_file = sys.argv[3]

    file1_reads = {}

    with open(input_file1, 'r') as f1:
        current_id = ''
        for raw_line in f1:
            line = trim(raw_line)

            if line.startswith('>'):
                current_id = line[1:]
            else:
                file1_reads[line] = current_id

    with open(input_file2, 'r') as f1, open(output_file, 'w+') as fo:
        current_id = ''
        for raw_line in f1:
            line = trim(raw_line)

            if line.startswith('>'):
                current_id = line[1:]
            else:
                if line in file1_reads:
                    fo.write(">%s\n" % (file1_reads[line] + current_id))
                    fo.write(line + "\n")


if __name__ == '__main__':
    main()
