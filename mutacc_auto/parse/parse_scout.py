import json
from datetime import datetime, timedelta
import logging

from mutacc_auto.commands.scout_command import ScoutExportCases
from mutacc_auto.parse.vcf_constants import (SCOUT_TO_FORMAT,
                                             SCOUT_TO_INFO,
                                             HEADER,
                                             NEWLINE,
                                             TAB,
                                             COLUMN_NAMES,
                                             SCOUT_TO_COLUMNS)

LOG = logging.getLogger(__name__)

#The timestamp in the scout database seems to be given with
#millisecond precision, it is therefor necessary to divide the
#timestamp with 1000 to make it compatible with the timestamp from
#the datetime module
TIMESTAMP_DIVIDE = 1000.0

class NoCausativesException(Exception):
    pass


def get_cases_from_scout(scout_output, days_ago=None):

    """
        Parses the scout output

        Args:
            scout_output (str): output from scout command
            days_ago (int): number of days since case updated

        Returns (list(dict)): list of dictionaries representing the cases
    """

    cases = json.loads(scout_output)

    if not days_ago:
        #Check if cases has causatives
        for case in cases:
            if not case.get('causatives'):
                LOG.warning(f"case {case['_id']} has no causatives")
                raise NoCausativesException

        return cases

    #MAKE DATETIME OBJECT days DAYS ago
    days_datetime = datetime.now() - timedelta(days=days_ago)

    recent_cases = []

    for case in cases:
        case_date = case['updated_at']['$date']
        case_date = datetime.fromtimestamp(case_date/TIMESTAMP_DIVIDE)
        if case_date > days_datetime and case.get('causatives'):
            recent_cases.append(case)

    return recent_cases





def get_vcf_from_json(scout_vcf_output):

    """
        Reconstructs vcf from scout variant object

        Args:
            scout_vcf_output (str): string returned by command 'scout export variants --json'

        Returns:
            vcf_string (str): string with vcf content
    """

    scout_vcf_output = json.loads(scout_vcf_output)

    vcf_string = ""

    #Write header of vcf
    for header_line in HEADER:
        vcf_string += header_line + NEWLINE

    #Get samples
    samples = [sample['sample_id'] for sample in scout_vcf_output[0]['samples']]

    #Append sample names to the COLUMN_NAMES list
    column_names = COLUMN_NAMES + samples
    column_names = TAB.join(column_names)

    vcf_string += column_names + NEWLINE

    #Write variants
    for variant in scout_vcf_output:

        #Write column values
        record = get_columns(variant)

        #write INFO
        info = get_info(variant)
        record.append(info)

        #Write the format a
        format = ':'.join([SCOUT_TO_FORMAT[ID] for ID in SCOUT_TO_FORMAT.keys()])
        record.append(format)

        #write genotypes for each sample
        samples = get_genotypes(variant)
        record.append(samples)

        record = TAB.join(record) + NEWLINE

        #Add variant record to vcf_string
        vcf_string += record

    return vcf_string

def get_columns(variant):
    """
        Given a variant object from scout, write the columns CHR - FILTER
        as a string with values separated by tab

        Args:
            variant (dict): dictionary of scout variant object
        Returns:
            record (str): values CHR-FILTER as a string
    """
    record = []

    for column in SCOUT_TO_COLUMNS:

        if type(variant[column]) == list:
            column_value = ','.join([str(element) for element in variant[column]])

        else:
            column_value = str(variant[column])

        record.append(column_value)

    return record

def get_info(variant):
    """
        Given a variant object from scout, write the INFO column
        for a variant.

        Args:
            variant (dict): dictionary of scout variant object
        Returns:
            info (str): INFO string
    """
    info = []
    for ID in SCOUT_TO_INFO.keys():

        info_string = f"{SCOUT_TO_INFO[ID]}={int(variant[ID])}"
        info.append(info_string)

    if variant['category'].lower() == 'snv':
        info_string = f"TYPE={variant['sub_category']}"

    else:
        info_string = f"SVTYPE={variant['sub_category']}"

    info.append(info_string)

    info = ';'.join(info)

    return info

def get_genotypes(variant):
    """
        Given a variant object from scout, write the genotypes column for each
        sample.

        Args:
            variant (dict): dictionary of scout variant object
        Returns:
            samples (str): genotypes for each sample
    """
    samples = []
    for sample in variant['samples']:

        gt_calls = []
        for ID in SCOUT_TO_FORMAT.keys():

            if type(sample[ID]) == list:

                ID_value = ','.join([str(element) for element in sample[ID]])

            else:
                ID_value = str(sample[ID])

            gt_calls.append(ID_value)

        gt_calls = ':'.join(gt_calls)
        samples.append(gt_calls)

    samples = TAB.join(samples)

    return samples
