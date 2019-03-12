import json
from datetime import datetime, timedelta

from mutacc_auto.commands.scout_command import ScoutExportCases
from mutacc_auto.parse.vcf_constants import *

#The timestamp in the scout database seems to be given with
#millisecond precision, it is therefor necessary to divide the
#timestamp with 1000 to make it compatible with the timestamp from
#the datetime module
TIMESTAMP_DIVIDE = 1000.0


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
        return cases

    #MAKE DATETIME OBJECT days DAYS ago
    days_datetime = datetime.now() - timedelta(days=days_ago)

    recent_cases = []

    for case in cases:
        case_date = case['updated_at']['$date']
        case_date = datetime.fromtimestamp(case_date/TIMESTAMP_DIVIDE)
        if case_date > days_datetime:
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
        vcf_string += header_line + '\n'

    #Get samples
    samples = [sample['sample_id'] for sample in scout_vcf_output[0]['samples']]
    samples = '\t'.join(samples)

    vcf_string += f"#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t{samples}\n"


    #Write variants
    for variant in scout_vcf_output:

        entry= []
        entry.append(str(variant['chromosome'])) #CHROM
        entry.append(str(variant['position'])) #POS
        entry.append(str(variant['dbsnp_id'] or '.')) #ID
        entry.append(str(variant['reference'])) #REF
        entry.append(str(variant['alternative'])) #ALT
        entry.append(str(variant['quality'])) #QUAL
        entry.append('PASS') #FILTER

        #write INFO
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

        entry.append(info)

        #Write the format and genotype calls
        format = ':'.join([SCOUT_TO_FORMAT[ID] for ID in SCOUT_TO_FORMAT.keys()])

        entry.append(format)

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

        samples = '\t'.join(samples)

        entry.append(samples)

        entry = '\t'.join(entry) + '\n'

        vcf_string += entry

    return vcf_string
