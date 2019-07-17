#!/bin/python3
################################################################################
# Politecnico di Torino, 2018 / 2019                                           #
# Bioinformatics (prof. Elisa Ficarra)                                         #
# Lab 1                                                                        #
# Assignment 1                                                                 #
#                                                                              #
# Luca Robbiano, 244033                                                        #
#                                                                              #
# This program generates a random fasta file. Example:                         #
# ./ex1_random_fasta.py 100 30 30 30 10 > random.fa                            #
# 100 is the number of reads, the other arguments are the probability weights  #
# for the bases A, T, C, G                                                     #
################################################################################

import sys
import random
from functools import reduce


def main():
    n = int(sys.argv[1])

    bases = "ATCG"
    weights = list(map(int, sys.argv[2:6]))

    for i in range(n):
        print(">read_id_%d" % i)
        seq = random.choices(bases, weights=weights, k=50)
        seq = reduce(lambda a, b: a + b, seq)
        print(seq)


if __name__ == '__main__':
    main()
