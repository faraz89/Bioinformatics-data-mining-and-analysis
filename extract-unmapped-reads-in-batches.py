import subprocess32
import os
import time
import sys

processes = set()
max_processes = 10

'''
Extract unmapped reads from the bam files and convert bam to fasta
Credits - Samtools is developed by John Marshall and Petr Danecek et al. Original author Heng Li
Seqtk Copyright (c) 2008-2012 by Heng Li <lh3@me.com>
'''

#import a file containing the names of all the bam files.
with open(sys.argv[1],'r') as k:
	bam_files = k.read().splitlines()
	
for bam in bam_files:
    output = bam.replace('.bam','.unmapped.bam')
    fasta_output = output.replace('.unmapped.bam','.unmapped.fasta')    
    cmd = 'samtools view -u -f 12 -F 256 %s > %s; samtools bam2fq %s | seqtk seq -A > %s' % (bam,output,output,fasta_output)
    processes.add(subprocess32.Popen([cmd], shell=True))
    print 'Submited job %s' % bam

    while True:
        jobs_running = len([p for p in processes if p.poll()==None])
        print jobs_running
        if jobs_running<max_processes:break
        os.wait()

#Check if all the child processes were closed
for p in processes:
    if p.poll() is None:
    	p.wait()
