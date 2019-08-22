#!/usr/bin/env python3

import yaml
import sys
from pathlib import Path
import logging

#Fields in a scout case document to be included as meta-data
SCOUT_CASE_FIELDS = (
    'genome_build',
    'genome_version',
    'dynamic_gene_list',
    'panels',
    'rank_model_version',
    'rank_score_threshold',
    'phenotype_terms',
    'phenotype_groups',
    'diagnosis_phenotypes',
    'diagnosis_genes'
)


LOG = logging.getLogger(__name__)

class NoBamException(Exception):
    pass

def get_case(case, vcf_file_path):

    case_id = case['_id']

    #Instatiate case dictionary with case_id
    case_obj = {
            'case_id': case_id
    }

    #Iterate over scout fields and add to case_obj.
    for field in SCOUT_CASE_FIELDS:

        if case.get(field):

            if field == 'panels':
                panels = [
                    {'display_name': panel.get('display_name'),
                     'panel_name': panel.get('panel_name')} for panel in case[field]
                ]
                case_obj[field] = panels
            else:
                case_obj[field] = case[field]

    #Get sample list
    samples_obj = assemble_samples(case['individuals'])

    return {

        'case': case_obj,
        'samples': samples_obj,
        'variants': vcf_file_path
    }


def assemble_samples(individuals):

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
        sex = 'unknown'
        if individual['sex'] == '1':
            sex = 'male'
        if individual['sex'] == '2':
            sex = 'female'

        samples.append(
            {
                'sample_id': individual['individual_id'],
                'sex': sex,
                'phenotype': 'affected' if (individual['phenotype'] == 2) else 'unaffected',
                'father': individual['father'] if individual['father'] else '0',
                'mother': individual['mother'] if individual['mother'] else '0',
                'analysis_type': individual['analysis_type'],
                'bam_file': individual['bam_file']
            }

        )


    return samples
