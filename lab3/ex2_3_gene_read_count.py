#!/bin/python3
################################################################################
# Politecnico di Torino, 2018 / 2019                                           #
# Bioinformatics (prof. Elisa Ficarra)                                         #
# Lab 3                                                                        #
# Assignment 2.3                                                               #
#                                                                              #
# Luca Robbiano, 244033                                                        #
#                                                                              #
# This program counts the reads for each gene. Example:                        #
# ./ex2_3_gene_read_count.py reference.gtf alignment.sam                       #
#                                                                              #
# NOTE: I'm not sure I implemented this in the right way. However the program  #
#       needs the library intervaltree                                         #
#       $ pip install intervaltree                                             #
################################################################################

import sys
import re
from intervaltree import IntervalTree


def main():
    gtf_ref_file = sys.argv[1]
    sam_file = sys.argv[2]

    r = re.compile(r'\s*;?\s+')

    genes = []
    genes_by_position = IntervalTree()

    print("Loading reference...")
    with open(gtf_ref_file, 'r') as fi:
        for raw_line in fi:
            if not raw_line.startswith('#!'):
                fields = r.split(raw_line)
                type = fields[2]
                if type == 'gene':
                    chromosome = trim(fields[0])
                    gene_id = trim(fields[fields.index('gene_id') + 1])
                    gene_name = trim(fields[fields.index('gene_name') + 1])
                    start_position = int(fields[3])
                    end_position = int(fields[4])
                    gene = Gene(chromosome, gene_id, gene_name)
                    genes.append(gene)
                    # end_position not included: I had to add one because IntervalTree does not support
                    # (x, x) intervals
                    genes_by_position.addi(start_position, end_position + 1, gene)

    print("Counting reads...")
    with open(sam_file, 'r') as fi:
        for raw_line in fi:
            fields = r.split(raw_line)
            chromosome = fields[2]
            position = int(fields[3])
            cigar = fields[5]
            ref_len = cigar_to_reference_length(cigar)  # Length of the reference segment
            interested_genes = genes_by_position[position:position + ref_len - 1] if ref_len != 1\
                else genes_by_position[position]
            for interested_gene_interval in interested_genes:
                # The end of the interval is not included. We need also to check if the chromosome is the same
                if position == interested_gene_interval.end or chromosome != gene.chromosome:
                    continue
                gene = interested_gene_interval.data
                gene.count = gene.count + 1

    for gene in genes:
        # Since there are a lot of genes without any read, let's print only the ones which have at least one read
        if gene.count != 0:
            print("%2s\t%-20s\t\t%-16s\t\t%d" % (gene.chromosome, gene.id, gene.name, gene.count))


# See https://samtools.github.io/hts-specs/SAMv1.pdf
# at 1.4.6 (page 7)
def cigar_to_reference_length(cigar_str):
    if cigar_str == '*':
        return 0
    r = re.compile(r'(\d+)([MIDNSHP=X])')
    operations = [(int(m.group(1)), m.group(2)) for m in r.finditer(cigar_str)]
    len = 0
    for op in operations:
        if op[1] in ['M', 'D', 'N', '=', 'X']:
            len += op[0]
    return len


class Gene:
    def __init__(self, chromosome, id, name):
        self.chromosome = chromosome
        self.id = id
        self.name = name
        self.count = 0


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
