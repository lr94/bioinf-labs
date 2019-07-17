#!/bin/python3
################################################################################
# Politecnico di Torino, 2018 / 2019                                           #
# Bioinformatics (prof. Elisa Ficarra)                                         #
# Lab 2                                                                        #
# Assignment 1                                                                 #
#                                                                              #
# Luca Robbiano, 244033                                                        #
#                                                                              #
# This program performs the global alignment of two strings of text using the  #
# Needleman-Wunsch algorithm. Example:                                         #
# ./ex1_global_alignment.py AACCG AACG 1 -1 -2                                 #
# 1, -1 and -2 are the values for match, mismatch and gap                      #
################################################################################

import sys
import numpy as np


def main():
    seq1 = sys.argv[1]
    len1 = len(seq1)
    h = len1 + 1
    seq2 = sys.argv[2]
    len2 = len(seq2)
    w = len2 + 1

    match_value = int(sys.argv[3])
    mismatch_value = int(sys.argv[4])
    gap_value = int(sys.argv[5])

    D = np.zeros((h, w))
    D[:, 0] = np.array(range(0, h * gap_value, gap_value))
    D[0, :] = np.array(range(0, w * gap_value, gap_value))

    traceback = np.zeros(D.shape + (2,), dtype=int)
    traceback[:, 0] = (-1, 0)
    traceback[0, :] = (0, -1)

    for i in range(1, h):
        for j in range(1, w):
            no_gap_score = D[i - 1, j - 1] + (match_value if seq1[i - 1] == seq2[j - 1] else mismatch_value)
            vgap_score = D[i - 1, j] + gap_value
            hgap_score = D[i, j - 1] + gap_value
            D[i, j] = no_gap_score
            traceback[i, j] = (-1, -1)
            if vgap_score > D[i, j]:
                D[i, j] = vgap_score
                traceback[i, j] = (-1, 0)
            if hgap_score > D[i, j]:
                D[i, j] = hgap_score
                traceback[i, j] = (0, -1)

    score = D[h - 1, w - 1]
    print("Global alignment score: %0.1f" % score)
    print(D)

    # Traceback to print alignment
    seq1_al = seq2_al = linking_lines = ''
    i = h - 1
    j = w - 1
    while i != 0 or j != 0:
        direction = traceback[i, j]
        i = i + direction[0]
        j = j + direction[1]
        if direction[0] == -1 and direction[1] == -1:
            linking_lines = ('|' if seq1[i] == seq2[j] else ' ') + linking_lines
            seq1_al = seq1[i] + seq1_al
            seq2_al = seq2[j] + seq2_al
        elif direction[0] == -1 and direction[1] == 0:
            linking_lines = ' ' + linking_lines
            seq1_al = seq1[i] + seq1_al
            seq2_al = '-' + seq2_al
        elif direction[0] == 0 and direction[1] == -1:
            linking_lines = ' ' + linking_lines
            seq1_al = '-' + seq1_al
            seq2_al = seq2[j] + seq2_al

    print("\nFinal alignment:")
    print(seq1_al)
    print(linking_lines)
    print(seq2_al)


if __name__ == '__main__':
    main()
