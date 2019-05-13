"""
    Functions to export synthetic dataset
"""

import logging
import json
import os
from pathlib import Path

from mutacc_auto.commands.mutacc_command import (MutaccExport, MutaccSynthesize)
from mutacc_auto.commands.vcf_command import (BgzipCommand, TabixCommand, BcftoolsMergeCommand)

LOG = logging.getLogger(__name__)


def run_mutacc_export_command(mutacc_config, mutacc_binary=None, case_query=None,
                              variant_query=None, proband=False, member='affected',
                              sample_name=None):

    """
        Runs the 'mutacc db export' command

        Args:
            mutacc_config (Path): Path to mutacc config file
            mutacc_binary (Path): path to mutacc binary
            case_query (string): json string with query against case collection
            variant_query (string): json string with query against variant collection
            proband (bool): True if sample is proband, False if not
            member (string): affected|father|mother|child
            sample_name (string): name of created sample

        returns:
            export_out (string): stdout from mutacc command

    """

    mutacc_export_command = MutaccExport(config_file=mutacc_config,
                                         mutacc_binary=mutacc_binary,
                                         case_query=case_query,
                                         variant_query=variant_query,
                                         proband=proband,
                                         member=member,
                                         sample_name=sample_name)
    export_out = mutacc_export_command.check_output()
    export_out = json.loads(export_out)
    return export_out

def export_trio(mutacc_config, mutacc_binary=None, case_query=None, variant_query=None):

    """
        Exports trio from mutaccDB

        Args:
            mutacc_config (Path): Path to mutacc config file
            mutacc_binary (Path): path to mutacc binary
            case_query (string): json string with query against case collection
            variant_query (string): json string with query against variant collection

        Returns:
            mutacc_files (dict): files created by mutacc for each sample

    """

    members = ('child', 'father', 'mother')
    mutacc_files = {}
    for member in members:

        member_files = run_mutacc_export_command(mutacc_config=mutacc_config,
                                                 mutacc_binary=mutacc_binary,
                                                 case_query=case_query,
                                                 variant_query=variant_query,
                                                 proband=True if member == 'child' else False,
                                                 member=member,
                                                 sample_name=member)

        mutacc_files[member] = member_files

    return mutacc_files

def bgzip_vcf_file(vcf_file):

    """
        Uses command line tool 'bgzip' to compress vcf

        Args:
            vcf_file (Path): path to vcf
        Returns:
            vcf_gz_file (Path): path to compressed vcf
    """

    zip_command = BgzipCommand(vcf_file)
    zip_command.call()
    return f"{vcf_file}.gz"

def index_vcf_file(vcf_file):

    """
        Uses command line tool 'tabix' to index vcf

        Args:
            vcf_file (Path): path to vcf
        Returns:
            vcf_index_file (Path): path to indexed vcf

    """

    index_command = TabixCommand(vcf_file)
    index_command.call()
    return f"{vcf_file}.tbi"

def merge_vcf_files(vcf_files, out_file=None):

    """
        Merges vcf files using 'bcftools merge'

        Args:
            vcf_files (list): list of paths to vcf files

        Returns:
            out_file (Path): path to merged vcf file
    """

    merge_command = BcftoolsMergeCommand(vcf_files, out_vcf=out_file)
    merge_command.call()
    return out_file

def synthesize_dataset(sample, mutacc_binary=None, mutacc_config=None):

    """
        Uses 'mutacc synthesize' to make synthetic dataset

        Args:
            sample (dict): Dictionary with fastq files, bam, and query file for sample
            mutacc_config (Path): Path to mutacc config file
            mutacc_binary (Path): path to mutacc binary

        Returns:
            dataset (list): list of fastq files created
    """

    synthesize_command = MutaccSynthesize(config_file=mutacc_config,
                                          mutacc_binary=mutacc_binary,
                                          fastq1=sample['fastq1'],
                                          fastq2=sample['fastq2'],
                                          bam_file=sample['bam'],
                                          query_file=sample['query'])

    dataset = synthesize_command.check_output()
    dataset = json.loads(dataset)['fastq_files']
    return dataset


def synthesize_trio(mutacc_config, samples, mutacc_binary=None):
    """
        Synthesizes a trio

        Args:
            mutacc_config (Path): Path to mutacc config file
            mutacc_binary (Path): path to mutacc binary
            samples (dict(dict)): fastq files, bam, query for each sample in trio

        Returns:
            datasets (dict): fastq files for each sample

    """
    datasets = {}
    for member in samples.keys():
        dataset = synthesize_dataset(mutacc_config=mutacc_config,
                                     mutacc_binary=mutacc_binary,
                                     sample=samples[member])
        datasets[member] = dataset

    return datasets


def export_dataset(mutacc_config, background=None, mutacc_binary=None, case_query=None,
                   variant_query=None, merged_vcf_path=None):

    """
        Export a synthetic trio

        Args:
            mutacc_config (Path): Path to mutacc config file
            mutacc_binary (Path): path to mutacc binary
            background (dict): dictionary with background files to be used for each sample
            case_query (string): json string with query against case collection
            variant_query (string): json string with query against variant collection
            merged_vcf_path (Path): path where to create vcf file

        Returns:
            datasets (dict): fastq files for each sample

    """

    files = export_trio(mutacc_config=mutacc_config,
                        mutacc_binary=mutacc_binary,
                        case_query=case_query,
                        variant_query=variant_query)

    vcf_files = [files[member]['vcf_file'] for member in files.keys()]
    zipped_vcf_files = [bgzip_vcf_file(vcf_file) for vcf_file in vcf_files]
    indexed_vcf_files = [index_vcf_file(vcf_file) for vcf_file in zipped_vcf_files]

    vcf_path = Path.cwd().joinpath('merged_mutacc_set.vcf.gz')
    if merged_vcf_path:
        vcf_path = merged_vcf_path

    vcf_path = merge_vcf_files(vcf_files=zipped_vcf_files, out_file=vcf_path)

    # Remove individual vcf files and their indices
    for zipped, indexed in zip(zipped_vcf_files, indexed_vcf_files):
        os.remove(zipped)
        os.remove(indexed)

    print("FILES: ", files)
    print("BACKGROUNDS: ", background)
    samples = {member: {'fastq1': background[member]['fastq1'],
                        'fastq2': background[member]['fastq2'],
                        'bam': background[member]['bam'],
                        'query': files[member]['query_file']} for member in files.keys()}

    datasets = synthesize_trio(mutacc_config=mutacc_config,
                               samples=samples,
                               mutacc_binary=mutacc_binary)

    return datasets
