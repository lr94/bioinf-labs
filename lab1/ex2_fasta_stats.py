#!/bin/python3
################################################################################
# Politecnico di Torino, 2018 / 2019                                           #
# Bioinformatics (prof. Elisa Ficarra)                                         #
# Lab 1                                                                        #
# Assignment 2                                                                 #
#                                                                              #
# Luca Robbiano, 244033                                                        #
#                                                                              #
# This program computes some stats about a fasta file and stores them in       #
# another file. Example:                                                       #
# ./ex2_fasta_stats.py input.fa output.txt                                     #
################################################################################

import sys

GC_THRESHOLD = 5


def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    bases = "ATCG"

    bases_stats = [0, 0, 0, 0]
    low_complexity_reads = 0
    gc_reads_count = 0
    gc_reads = []

    with open(input_file, 'r') as input, open(output_file, 'w+') as output:
        lines = input.read().splitlines()

        current_id = ''
        for current_line in lines:
            if current_line.startswith('>'):
                current_id = current_line[1:]
            else:
                # Base stats
                for current_base in current_line:
                    if current_base == 'A':
                        bases_stats[0] = bases_stats[0] + 1
                    if current_base == 'T':
                        bases_stats[1] = bases_stats[1] + 1
                    if current_base == 'C':
                        bases_stats[2] = bases_stats[2] + 1
                    if current_base == 'G':
                        bases_stats[3] = bases_stats[3] + 1

                # Low complexity
                if ('A' * 6) in current_line or ('T' * 6) in current_line or ('C' * 6) in current_line or ('G' * 6) in current_line:
                    low_complexity_reads = low_complexity_reads + 1

                # GC content
                gcn = current_line.count('GC')
                if gcn > GC_THRESHOLD:
                    gc_reads_count = gc_reads_count + 1
                    gc_reads.append({'id': current_id, 'count': gcn})

        for i in range(4):
            output.write("Base %c: %d\n" % (bases[i], bases_stats[i]))

        output.write("Reads having at least one low complexity sequence: %d\n" % low_complexity_reads)

        output.write("Reads with gc content: %d\n" % gc_reads_count)

        for current_element in gc_reads:
            output.write("\t%s: %d GC couples\n" % (current_element['id'], current_element['count']))


if __name__ == '__main__':
    main()
