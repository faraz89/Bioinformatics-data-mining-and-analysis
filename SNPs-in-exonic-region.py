#!/usr/bin/env python
# coding: utf-8
# AUTHORS: Faraz Khan and Cullen Rhodes

import subprocess
import os
import time
import sys
from collections import defaultdict

'''
This script takes input the coordinates of all the exons from gff file of species of interest and the coordinates of all the snps generated from the variant caller. This script find all the SNPs that lie in the exonic region of the genome.
'''

#Note. The coordinates needs to be sorted.
exons_coords = sys.argv[1]
snp_coords = sys.argv[2]

d = defaultdict(list)
with open(exons_coords) as f:
    for line in f.readlines():
        key, start, end = line.split()
        d[key].append((int(start), int(end)))


def Approach_one():
    with open(snp_coords) as f:
        for line in f.readlines():
            key, target_pos, snp1, snp2 = line.split()
            target_pos = int(target_pos)
            key_ranges = d[key]
            for (start, end) in key_ranges:
                if start <= target_pos <= end:
                    print key,target_pos,snp1,snp2

def Approach_two():
    with open(snp_coords) as f:
        key = 'Chromosome01'
        key_ranges = d[key]
        highest_idx = 0
        for line in f.readlines():
            key2, target_pos, snp1, snp2 = line.split()
            if key != key2:
                highest_idx = 0
                key = key2
                key_ranges = d[key]
            target_pos = int(target_pos)
            for idx, (start, end) in enumerate(key_ranges[highest_idx:]):
                if start <= target_pos <= end:
                    if idx > highest_idx:
                        highest_idx = idx
                    print(key, start, target_pos, end, snp1, snp2)


if __name__ == '__main__':
    Approach_one()
