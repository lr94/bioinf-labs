#!/usr/bin/env bash
################################################################################
# Politecnico di Torino, 2018 / 2019                                           #
# Bioinformatics (prof. Elisa Ficarra)                                         #
# Lab 2                                                                        #
# Assignment 4                                                                 #
#                                                                              #
# Luca Robbiano, 244033                                                        #
#                                                                              #
# This scripts performs the alignment of two mates using BWA with a            #
# reference. The result is stored in a SAM file. Example:                      #
# ./ex4_bwa_alignment.sh ref.fa mate1.fa mate2.fa out.sam                      #
################################################################################

echo "BWA initializing..."

TMPDIR=/tmp/bwa_index/
REF=$1
M1=$2
M2=$3
OUT=$4

mkdir -p "${TMPDIR}"

bwa index -p "${TMPDIR}" "${REF}" &>/dev/null

echo "BWA aligner is currently running. This step could require time, be patient!"
bwa mem "${TMPDIR}" "${M1}" "${M2}" > "${OUT}" 2>/dev/null

rm -rf "${TMPDIR}"