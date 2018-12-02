import subprocess
import os
import time
import sys

processes = set()
max_processes = 10

'''
Script to run Adapter and quality trimming of Illumina data in small batches.

'''

#import a text file containing file names of forward reads. 
with open(sys.argv[1],'r') as k:
	R1_file = k.read().splitlines()
	
for R1 in R1_file:
    #replace R1 to R2 for reverse reads.  
    R2 = R1.replace('_R1.fastq.gz','_R2.fastq.gz')
    #run cutadapt with the file for the list of adapters used. In this case all the Nextera adapters will be trimmed.
    cmd = 'cutadapt -a file:NexteraPE-PE.fa -A file:NexteraPE-PE.fa -m 40 -q 20 -o qatrimmed_%s -p qatrimmed_%s %s %s' % (R1,R2,R1,R2)
    processes.add(subprocess.Popen([cmd], shell=True))
    print 'Submited job %s %s' % (R1,R2)

    while True:
        jobs_running = len([p for p in processes if p.poll()==None])
	 print jobs_running
        if jobs_running<24:break
        os.wait()
        #24 jobs will run at a time.

#Check if all the child processes were closed
for p in processes:
    if p.poll() is None:
    	p.wait()


