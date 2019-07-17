#!/bin/python3
################################################################################
# Politecnico di Torino, 2018 / 2019                                           #
# Bioinformatics (prof. Elisa Ficarra)                                         #
# Lab 4                                                                        #
# Assignment 1                                                                 #
#                                                                              #
# Luca Robbiano, 244033                                                        #
#                                                                              #
# This program performs differential gene analysis using t-test and stores the #
# selected features in a reduced dataset                                       #
################################################################################

import sys
import pandas as pd
import numpy as np
import scipy.stats as stats
import re
import requests

alpha = 0.05


def main():
    dataset_file = sys.argv[1]
    output_file = sys.argv[2]

    # Load dataset
    dataset = pd.read_csv(dataset_file)
    genes = list(dataset.columns[1:])
    G = len(genes)
    dataset['l'] = dataset['l'].str.strip()  # Remove trailing spaces from "Luminal A" and "Luminal B"
    samples_A = dataset[dataset['l'] == 'Luminal A']
    samples_B = dataset[dataset['l'] == 'Luminal B']

    selected_genes = []
    # For each gene
    for gene in genes:
        lum_A = samples_A[gene]
        lum_B = samples_B[gene]
        # Welch T-Test (with Bonferroni adjustment)
        t_value, p_value = stats.ttest_ind(np.array(lum_A), np.array(lum_B), equal_var=False)
        if p_value < alpha / G:
            # Reject null hypothesis
            selected_genes.append(gene)

    reduced_dataset = dataset[['l'] + selected_genes]
    reduced_dataset = reduced_dataset.rename(lambda g: g if g == 'l' else ensg_to_common_name(g), axis='columns')
    reduced_dataset.to_csv(output_file, index=False)

    print("Selected %d / %d genes" % (len(selected_genes), len(genes)))
    selected_genes_common_names = list(reduced_dataset.columns)[1:]
    for sgcn in selected_genes_common_names:
        print("\t%s" % sgcn)


def ensg_to_common_name(ensg):
    r = re.compile("([A-Z\\d]+)(?:\\.\\d+)?")
    m = r.match(ensg)
    if m is None:
        return None
    ensg = m.group(1)  # Remove version if present
    url = "https://rest.ensembl.org/overlap/id/%s?feature=gene" % ensg
    req = requests.get(url, headers={
        'Content-Type': 'application/json'
    })
    if not req.ok:
        return '[%s]' % ensg  # Request error
    decoded = req.json()
    if len(decoded) == 0:
        return '[%s]' % ensg  # Not found
    return decoded[0]['external_name']


if __name__ == '__main__':
    main()