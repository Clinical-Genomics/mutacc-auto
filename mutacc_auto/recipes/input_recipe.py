import yaml
from pathlib import Path
import subprocess
import logging

from mutacc_auto.utils.tmp_dir import TemporaryDirectory
from mutacc_auto.commands.scout_command import ScoutExportCases, ScoutExportCausativeVariants
from mutacc_auto.commands.housekeeper_command import HousekeeperCommand
from mutacc_auto.parse.parse_scout import get_cases_from_scout
from mutacc_auto.parse.parse_variant import get_vcf_from_json
from mutacc_auto.parse.parse_housekeeper import get_bams_from_housekeeper
from mutacc_auto.build_input.input_assemble import (get_case, NoBamException)

PADDING = 600

LOG = logging.getLogger(__name__)

def get_cases(case_id = None, days_ago = None, scout_config=None, scout_binary=None):

    """
        Get cases from scout

        Args:
            case_id (str): case id
            days_ago (int): days since update

        Returns:
            cases (list(dict)): list of cases represented as dictionaries
    """
    scout_case_command = ScoutExportCases(
        case_id = case_id,
        config_file=scout_config,
        scout_binary=scout_binary
    )
    scout_output = scout_case_command.check_output()
    cases = get_cases_from_scout(scout_output, days_ago)

    return cases

def get_bams(case_id, hk_config=None, hk_binary=None):

    """
        Get bam files from housekeeper

        Args:
            case_id (str): case id

        Returns:
            bam_paths (dict): dict with paths to bam for each sample
    """

    #housekeeper_command = HousekeeperCommand(
    #    case_id=case_id,
    #    config_file=hk_config,
    #    hk_binary=hk_binary
    #)
    #hk_output = housekeeper_command.check_output()
    ###
    hk_out = subprocess.check_output(['cat', '/Users/adam.rosenbaum/develop/mutacc_auto/tests/fixtures/HK_output_test.txt'])
    hk_output = hk_out.decode('utf-8')
    ###
    bam_paths = get_bams_from_housekeeper(hk_output)

    return bam_paths

def write_vcf(case_id, directory, scout_config=None, scout_binary=None):

    """
        Writes vcf file from scout output

        case_id (str): case id
        directory (path): path to write vcf_file
    """

    with open(
        Path(directory).joinpath("{}_causatives.vcf".format(case_id)),
        'w'
        ) as vcf_handle:

        vcf_command = ScoutExportCausativeVariants(
            case_id,
            config_file=scout_config,
            scout_binary=scout_binary
        )
        vcf_scout_output = vcf_command.check_output()
        vcf_content = get_vcf_from_json(vcf_scout_output)
        vcf_handle.write(vcf_content)

        vcf_path = vcf_handle.name

        return vcf_path

def write_input(case_dict, directory):

    """
        Writes the input case file (yaml)

        Args:
            case_dict (dict): dictionary with case info
            directory (path): path to directory where file is written
    """

    case_id = case_dict['case']['case_id']

    with open(
            Path(directory).joinpath("{}_input.yaml".format(case_id)),
            'w'
        ) as input_handle:

        yaml.dump(case_dict, input_handle, default_flow_style=False)
        input_path = input_handle.name

        return input_path

def get_analysis_type(case):

    """
        Given a case object, find analysis type (WES or WGS)

    """

    analysis_type = 'wgs'
    for sample in case['individuals']:

        if sample['analysis_type'].lower() == 'wes':

            analysis_type = 'wes'
            break

    return analysis_type

def get_inputs(tmp_dir ,case_id = None, days_ago = None, padding = None,
    scout_config=None, scout_binary=None, hk_config=None, hk_binary = None):

    """
        Get input data for each case

        Args:
            tmp_dir (path): path to temporary directory where all files are writtten
            case_id (str): case id
            days_ago (int): days since last update
            padding (int): padding of genomic region

        Returns
            inputs (list(dict)): List of dictionaries with path to input file,
                                 and padding for each case
    """
    cases = get_cases(case_id, days_ago, scout_config=scout_config, scout_binary=scout_binary)

    inputs = []

    for case in cases:

        input_dict = {}

        #case_id = case['display_name']
        case_id = case['_id']

        bam_paths = get_bams(case_id, hk_config=hk_config, hk_binary=hk_binary)

        vcf_path = write_vcf(case_id, tmp_dir, scout_config=scout_config, scout_binary=scout_binary)

        try:
            case_dict = get_case(case, bam_paths, vcf_path)
        except NoBamException:
            LOG.warning(f"Missing bam files for case {case['_id']}")
            continue

        input_path = write_input(case_dict, tmp_dir)

        input_dict['input_file'] = input_path

        analysis_type = get_analysis_type(case)

        if analysis_type == 'wes':
            padding = 0
        elif analysis_type == 'wgs':
            padding = padding or PADDING

        input_dict['padding'] = padding

        inputs.append(input_dict)

    return inputs
