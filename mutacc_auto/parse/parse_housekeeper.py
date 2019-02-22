from mutacc_auto.commands.housekeeper_command import HousekeeperCommand

def get_bams_from_housekeeper(housekeeper_output):

    bam_files = {}

    #CHECK FOR FILES WITH 'BAM' TAG AND STORE IN DICTIONARY
    for row in housekeeper_output.split('\n'):

        fields = row.split('|')

        tags = fields[-1].split(',')

        if len(tags) == 2 and tags[0].strip() == 'bam':

            sample = tags[-1].strip()

            bam_files[sample] = fields[1].strip()


    return bam_files
