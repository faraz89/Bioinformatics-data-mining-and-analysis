import subprocess32
import os
import time

processes = set()
max_processes = 10

"""
    Run Bowtie Aligner in batches
    Bowtie is developed by Ben Langmead et al.
    Credits - Samtools is developed by John Marshall and Petr Danecek et al. Original author Heng Li.
"""

#Open file containing file names of forward reads.
with open(sys.argv[1],'r') as k:
	R1fastq_files = k.read().splitlines()
	
for R1 in R1fastq_files:
    #Replace R1 to R2 for reverse reads.
    R2 = R1.replace('_R1.fastq.gz','_R2.fastq.gz')
    #Change fastq extension to bam for bam output.
    bams = R1.replace('_R1.fastq.gz','.sorted.bam') 
    cmd = 'bowtie2 -1 %s -2 %s -x Mes_bowtie -p 6 --end-to-end --sensitive | samtools view -bS - | samtools sort -@ 6 -o %s -' % (R1,R2,bams)
    print cmd    
    processes.add(subprocess32.Popen([cmd], shell=True))
    print 'Submited job %s' % cmd

    while True:
        jobs_running = len([p for p in processes if p.poll()==None])
	print jobs_running
        if jobs_running<max_processes:break
        os.wait()

#Check if all the child processes were closed
for p in processes:
    if p.poll() is None:
    	p.wait()
