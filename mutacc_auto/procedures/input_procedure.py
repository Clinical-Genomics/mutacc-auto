import yaml
from pathlib import Path
import subprocess
import logging

from mutacc_auto.utils.tmp_dir import TemporaryDirectory
from mutacc_auto.parse.parse_variant import get_vcf_from_json
from mutacc_auto.build_input.input_assemble import get_case

PADDING = 600

LOG = logging.getLogger(__name__)

def write_vcf(directory, variants: str, case_id: str):

    """
        Writes vcf file from scout output

        case_id (str): case id
        directory (path): path to write vcf_file
    """

    with open(Path(directory).joinpath(f"{case_id}_causatives.vcf"), 'w') as vcf_handle:


        vcf_content = get_vcf_from_json(variants)
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

    with open(Path(directory).joinpath("{}_input.yaml".format(case_id)), 'w') as input_handle:

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

def get_input(tmp_dir ,case, variants, padding = None):

    """
        Get input data for each case

        Args:
            tmp_dir (Path): Path to keep temporary files
            case (dict): Case information from scout
            variants (list): Causative variants from scout
            padding (int): padding of genomic region

        Returns
            input (list(dict)): List of dictionaries with path to input file,
                                 and padding for each case
    """

    input_dict = {}

    case_id = case['_id']
    input_dict['case_id'] = case_id
    vcf_path = write_vcf(tmp_dir, variants, case_id)
    case_dict = get_case(case, vcf_path)
    input_path = write_input(case_dict, tmp_dir)
    input_dict['input_file'] = input_path
    analysis_type = get_analysis_type(case)

    #if analysis_type == 'wes':
    #    padding = 0
    #elif analysis_type == 'wgs':
    #    padding = padding or PADDING

    input_dict['padding'] = padding or PADDING


    return input_dict
