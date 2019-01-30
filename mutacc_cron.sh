#!/bin/bash

#This bash script is to be executed with crontab.

OUTPUT_DIR = /.../.../
LOG_FILE = /.../.../...

#Generate input files to mutacc with cases updated DAYS_AGO(int) days ago
#and place vcf and yaml files in OUTPUT_DIR
python ./input_assemble $DAYS_AGO $OUTPUT_DIR

#For each input yaml file created, pass them to the sbatch bash script
#Where the reads from the bam files are extracted and placed on disk
for case_input in $OUTPUT_DIR/*.yaml
do
    sbatch ...
done

#Remove all input files + vcf
rm $OUTPUT_DIR/*

#Import Cases into mutaccDB 
for import_file in $IMPORT_DIR/*.mutacc
do
  mutacc db import import_file 2> $LOG_FILE
done

rm $IMPORT_DIR/*.mutacc
