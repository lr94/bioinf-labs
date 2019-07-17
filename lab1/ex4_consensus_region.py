#!/bin/python3
################################################################################
# Politecnico di Torino, 2018 / 2019                                           #
# Bioinformatics (prof. Elisa Ficarra)                                         #
# Lab 1                                                                        #
# Assignment 4                                                                 #
#                                                                              #
# Luca Robbiano, 244033                                                        #
#                                                                              #
# This program finds the maximum consensus region between all the reads in a   #
# fasta file. Example:                                                         #
# ./ex4_consensus_region.py input.py 0                                         #
# Where 0 is the maximum allowed number of mismatches                          #
#                                                                              #
# NOTE: Probably this program is very inefficient, I don't think I used the    #
#       best algorithm for the task.                                           #
#       The program requires the package regex to be installed:                #
#       $ pip install regex                                                    #
################################################################################

import sys
import regex


def main():
    input_file = sys.argv[1]
    max_mismatches = int(sys.argv[2])

    # Load all the reads (and find the shortest one)
    reads = []
    shortest_index = index = 0
    with open(input_file, 'r') as input:
        for current_raw_line in input:
            line = trim(current_raw_line)
            if not line.startswith('>'):
                reads.append(line)
                if len(line) < len(reads[shortest_index]):
                    shortest_index = index
                index = index + 1

    # Pick the shortest read, removing it from the list
    shortest_seq = reads.pop(shortest_index)

    # Starting from the length of the shortest read we try all its substrings to see if they are consensus regions
    for candidate_length in range(len(shortest_seq), 1, -1):
        substrings = generate_substrings(shortest_seq, candidate_length)
        for current_candidate in substrings:
            mismatches = 0
            ok = True
            for current_read in reads:
                r = regex.compile('(%s){s<=%d}' % (current_candidate, max_mismatches))
                result = r.search(current_read)
                if result is None:
                    ok = False
                    break
                if result.fuzzy_counts[0] > mismatches:
                    mismatches = result.fuzzy_counts[0]
            if ok:
                print("%s length: %d mismatches: %d" % (current_candidate, len(current_candidate), mismatches))
                return

    print("No consensus region")


# Generate all the possible k-substrings of string
def generate_substrings(string, k):
    arr = []
    str_len = len(string)
    i = 0
    while i + k <= str_len:
        arr.append(string[i:i + k])
        i = i + 1

    return arr


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


if __name__ == '__main__':
    main()
