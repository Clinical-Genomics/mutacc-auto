import yaml
from pathlib import Path
import subprocess

from mutacc_auto.utils.tmp_dir import TemporaryDirectory
from mutacc_auto.commands.scout_command import ScoutExportCases, ScoutExportCausativeVariants
from mutacc_auto.commands.housekeeper_command import HousekeeperCommand
from mutacc_auto.parse.parse_scout import get_cases_from_scout
from mutacc_auto.parse.parse_housekeeper import get_bams_from_housekeeper
from mutacc_auto.build_input.input_assemble import get_case

PADDING = 600

def get_cases(case_id = None, days_ago = None):

    """
        Get cases from scout

        Args:
            case_id (str): case id
            days_ago (int): days since update

        Returns:
            cases (list(dict)): list of cases represented as dictionaries
    """
    scout_case_command = ScoutExportCases(case_id = case_id)
    scout_output = scout_case_command.check_output()
    cases = get_cases_from_scout(scout_output, days_ago)

    return cases

def get_bams(case_id):

    """
        Get bam files from housekeeper

        Args:
            case_id (str): case id

        Returns:
            bam_paths (dict): dict with paths to bam for each sample
    """

    housekeeper_command = HousekeeperCommand(case_id=case_id)
    hk_output = housekeeper_command.check_output()
    ###
    #hk_out = subprocess.check_output(['cat', '/Users/adam.rosenbaum/develop/mutacc_auto/tests/fixtures/HK_output_test.txt'])
    #hk_output = hk_out.decode('utf-8')
    ###
    bam_paths = get_bams_from_housekeeper(hk_output)

    return bam_paths

def write_vcf(case_id, directory):

    """
        Writes vcf file from scout output

        case_id (str): case id
        directory (path): path to write vcf_file
    """

    with open(
        Path(directory).joinpath("{}_causatives.vcf".format(case_id)),
        'w'
        ) as vcf_handle:

        vcf_command = ScoutExportCausativeVariants(case_id)
        vcf_content = vcf_command.check_output()
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

def get_inputs(tmp_dir ,case_id = None, days_ago = None, padding = None):

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
    cases = get_cases(case_id, days_ago)

    inputs = []

    for case in cases:

        input_dict = {}

        case_id = case['display_name']

        bam_paths = get_bams(case_id)

        vcf_path = write_vcf(case_id, tmp_dir)

        case_dict = get_case(case, bam_paths, vcf_path)

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
