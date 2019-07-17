#!/bin/python3
################################################################################
# Politecnico di Torino, 2018 / 2019                                           #
# Bioinformatics (prof. Elisa Ficarra)                                         #
# Lab 3                                                                        #
# Assignment 1.4                                                               #
#                                                                              #
# Luca Robbiano, 244033                                                        #
#                                                                              #
# This program should (?) parse a VCF file and obtain only the Single          #
# Nucleotides Polymorphisms for which the information is complete. Example:    #
# ./ex1_4_snp.py input.vcf filtered_snp.vcf                                    #
#                                                                              #
# NOTE: I'm not sure if I implemented this in the right way                    #
################################################################################

import sys
import re


def main():
    vcf_input_file = sys.argv[1]
    vcf_output_file = sys.argv[2]
    r_header = re.compile('#[^#].*')
    r_splitter = re.compile('\\s+')

    kept = counter = 0
    pos_index = ref_index = alt_index = -1

    with open(vcf_input_file, 'r') as fi, open(vcf_output_file, 'w+') as fo:
        for raw_line in fi:
            counter = counter + 1
            # Parse header
            if r_header.match(raw_line):
                fo.write(raw_line)
                fields = r_splitter.split(raw_line[1:])
                pos_index = fields.index('POS')
                ref_index = fields.index('REF')
                alt_index = fields.index('ALT')
            elif pos_index * ref_index * alt_index >= 0:  # Header already parsed
                fields = r_splitter.split(raw_line)
                # TODO check if this is the right way
                # position = fields[pos_index]
                # ref = fields[ref_index]
                alt = fields[alt_index]
                if alt != '<*>':
                    fo.write(raw_line)
                    kept = kept + 1
            elif raw_line.startswith('##'):
                fo.write(raw_line)

        print("Kept %d / %d reads" % (kept, counter))


if __name__ == '__main__':
    main()
