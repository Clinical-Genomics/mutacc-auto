#!/usr/bin/env python3

import yaml
import sys
from pathlib import Path
import logging


from mutacc_auto.subprocessing import scout_call
from mutacc_auto.subprocessing import hk_call

LOG = logging.getLogger(__name__)

class NoBamException(Exception):
    pass

def assemble_case(case, directory):
    """
        Given an case id, assembles mutacc input file in yaml format
        for case if all necessary information is found through scout and
        housekeeper.

        Args:
            case(dict): case object from scout query
            directory(pathlib.Path): Path to directory where yaml is stored

    """
    case_id = case['display_name']

    case_obj = {
        'case_id': case_id
    }

    bam_files = hk_call.find_bams(case_id)

    if len(bam_files.keys()) == 0:

        LOG.critical("No BAM-files found for case {}".format(case_id))
        raise NoBamException

    samples_obj = assemble_samples(case['individuals'], bam_files)

    vcf_file = scout_call.create_vcf(case_id, directory)

    with open(directory.joinpath("{}_mutacc_input.yaml".format(case_id)), 'w') as case_handle:

        yaml.dump(
            {
            'case': case_obj,
            'samples': samples_obj,
            'variants': vcf_file
            },
            case_handle,
            default_flow_style=False
        )
        case_file_name = case_handle.name


    return case_file_name


def assemble_samples(individuals, bam_files = None):

    """
        Given a list of individuals, this function assembles a samples object
        for the 'samples' field in the input YAML file

        Args:
            individuals(list): list of individuals from scout query
            bam_files(dict): dictionary with bam_files for each sample

        Returns:
            samples(list): list with sample objects

    """
    samples = []

    for individual in individuals:
        samples.append(
            {
                'sampe_id': individual['individual_id'],
                'sex': 'male' if (individual['sex'] == '1') else 'female',
                'phenotype': 'affected' if (individual['phenotype'] == 2) else 'unaffected',
                'father': individual['father'],
                'mother': individual['mother'],
                'analysis_type': individual['analysis_type'],
                'bam_file': bam_files.get(individual['individual_id']) if bam_files else None
            }

        )
        #Check if bam_file is found for each sample
        if not samples[-1]['bam_file']:
            LOG.critical("No bam file found for sample {}".format(individual['individual_id']))
            raise NoBamException


    return samples

if __name__ == '__main__':
    #GET ARGUMENTS FROM COMMAND LINE
    days = int(sys.argv[1])

    #Checks if directory exists
    directory = Path(str(sys.argv[2])).expanduser().absolute()
    if not directory.is_dir():
        LOG.critical("No such directory")
        raise IOError

    #FIND ALL CASES UPDATED days DAYS ago
    cases = scout_call.find_cases_since(days=days)

    #ASSEMBLE INPUT YAML FILE AND VCF FILE FOR EACH CASE FOUND
    for case in cases:

        assemble_case(case, directory)
