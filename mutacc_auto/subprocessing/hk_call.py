import subprocess
import json
import sys

def find_bams(case):

    """
    Finds paths to BAM-files for case in HouseKeeper
    Args:
        case_id (str): case ID of sample in HouseKeeper


    Returns:

        bam_files (dictionary): dictionary with sample name as keys,
                                and BAM-path as values.


    """

    #USE HK OUTPUT FROM FILE IF RUNNED AS TEST
    if 'pytest' in sys.modules.keys():
        hk_out = subprocess.check_output(['cat', 'mutacc_auto/tests/fixtures/HK_output_test.txt'])

    else:
        pass
        #hk_out = subprocess.check_output(['housekeeper','get', '-V', case])
    #GET FILES FOR CASE FROM HOUSEKEEPER
    hk_out = subprocess.check_output(['cat', 'mutacc_auto/tests/fixtures/HK_output_test.txt'])
    #hk_out = subprocess.check_output(['cat', 'mutacc_auto/tests/fixtures/HK_output_test_wrong_bam.txt'])
    #hk_out = subprocess.check_output(['cat', 'mutacc_auto/tests/fixtures/HK_output_test_no_bam.txt'])
    #hk_out = subprocess.check_output(['housekeeper','get', '-V', case])

    hk_out = hk_out.decode("utf-8")

    bam_files = {}

    #CHECK FOR FILES WITH 'BAM' TAG AND STORE IN DICTIONARY
    for row in hk_out.split('\n'):

        fields = row.split('|')

        tags = fields[-1].split(',')

        if len(tags) == 2 and tags[0].strip() == 'bam':

            sample = tags[-1].strip()

            bam_files[sample] = fields[1].strip()


    return bam_files



if __name__ == "__main__":

    case_id = sys.argv[1]

    hk_files = find_bams(case_id)

    print(hk_files)
