#!/usr/bin/env python
# coding: utf-8
# AUTHOR: Faraz Khan

import subprocess
import os
import time
import sys

processes = set()
max_processes = 10

#import a file containing the names of all the bam files.
with open(sys.argv[1],'r') as k:
    bam_files = k.read().splitlines()

#import a file containing all Chromosomes IDs (without '>') from your reference genome.
with open(sys.argv[2],'r') as v:
    intervals = v.read().splitlines()

for interval in range(len(intervals)):
    interval = intervals[interval].splitlines()
    for j in bam_files:
        interval2 = ''.join(interval)
        interval2.replace('[]','')
        input_tag = j
        input_tag = input_tag.replace('.sorted_RG_nodup.bam','') #here I am trimming some strings from the name of the bam files. Rationale is to have just an identifier that can make each bam file distinct.
        #Run GATK HaplotypeCaller using Cassava Reference genome. You can replace the "cassava-v7.fasta" with your genome of interest.
        cmd = "gatk HaplotypeCaller -ERC GVCF --native-pair-hmm-threads 5 -R cassava-v7.fasta -I "+j+" --output "+input_tag+"_"+str(interval2)+".g.vcf -L "+str(interval2)
        processes.add(subprocess.Popen([cmd], shell=True))
        print 'Submited job %s' % cmd

        while True:
            jobs_running = len([p for p in processes if p.poll()==None])
	    print jobs_running
            if jobs_running<24:break
            os.wait()

#Check if all the child processes were closed
for p in processes:
    if p.poll() is None:
        p.wait()
