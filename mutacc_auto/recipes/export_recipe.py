import logging
import json
import os
from pathlib import Path

from mutacc_auto.commands.mutacc_command import MutaccExport
from mutacc_auto.commands.vcf_command import (BgzipCommand, TabixCommand, BcftoolsMergeCommand)

LOG = logging.getLogger(__name__)


def run_mutacc_export_command(mutacc_config, mutacc_binary=None, case_query=None, variant_query=None,
                              proband=False, member='affected', sample_name=None):

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

    zip_command = BgzipCommand(vcf_file)
    zip_command.call()
    return f"{vcf_file}.gz"

def index_vcf_file(vcf_file):

    index_command = TabixCommand(vcf_file)
    index_command.call()
    return f"{vcf_file}.tbi"

def merge_vcf_files(vcf_files, out_file=None):

    merge_command = BcftoolsMergeCommand(vcf_files, out_vcf=out_file)
    merge_command.call()
    return out_file

def export_datasets(mutacc_config, mutacc_binary=None, case_query=None, variant_query=None,
                    merged_vcf_path=None):

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

    return vcf_path
