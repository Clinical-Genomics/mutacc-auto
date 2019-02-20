import subprocess
import json
from datetime import datetime, timedelta
import sys



def create_vcf(case_id, directory):
    """
        Ceates VCF-file of the causative variants for case-id

        Args:
            case_id(str): ID of case
            directory(pathlib.Path): Path to directory where vcf is placed
    """

    causatives_vcf = subprocess.check_output(
        [
            'scout',
            'export',
            'variants',
            '--case-id',
            case_id
        ]
    )

    with open(directory.joinpath("{}_causatives.vcf".format(case_id)),'wb') as causatives_handle:

        causatives_handle.write(causatives_vcf)
        vcf_file_name = causatives_handle.name

    return vcf_file_name



def find_cases_since(days=1):
    """
    Finds cases updated the past days

    Args:

        days(int): number of days to check since update

    Returns:

        recent_cases(list): list of cases

    """

    #MAKE DATETIME OBJECT days DAYS ago
    days_datetime = datetime.now() - timedelta(days=days)

    #FIND SOLVED CASES FROM SCOUT
    solved_cases = subprocess.check_output(
        [
            'scout',
            'export',
            'cases',
            '--json',
            '--finished',
        ]
    )

    solved_cases = json.loads(solved_cases.decode("utf-8"))

    recent_cases = []

    #CHECK IF CASE HAS BEEN UPDATED LATER THAN days DAYS AGO
    for case in solved_cases:
        case_date = case['updated_at']['$date']
        case_date = datetime.fromtimestamp(case_date/1000.0)
        if case_date > days_datetime:
            recent_cases.append(case)

    return recent_cases

def find_cases(case_id):

    case = subprocess.check_output(
        [
            'scout',
            'export',
            'cases',
            '--json',
            '--case-id',
            case_id
        ]
    )

    case = json.loads(case.decode("utf-8"))


    return case

if __name__ == '__main__':


    days = int(sys.argv[1])
    print(find_cases_since(days=days))

    case_id = str(sys.argv[2])
