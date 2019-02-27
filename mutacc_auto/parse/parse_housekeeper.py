from mutacc_auto.commands.housekeeper_command import HousekeeperCommand

def get_bams_from_housekeeper(housekeeper_output):

    """
        parses housekeeper output to find the bam files for each sample

        Args:
            housekeeper_output (str): Output from running the Housekeeper command

        Returns:
            bam_files (dict): dictionary with sample names as keys, holding
                              bam file for each sample in the case.
    """

    bam_files = {}

    #CHECK FOR FILES WITH 'BAM' TAG AND STORE IN DICTIONARY
    for row in housekeeper_output.split('\n'):

        fields = row.split('|')

        tags = fields[-1].split(',')

        tag = tags[0].strip()

        if len(tags) == 2 and tag == 'bam':

            sample = tags[-1].strip()

            bam_files[sample] = fields[1].strip()


    return bam_files
