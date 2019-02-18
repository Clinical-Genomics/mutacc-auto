import subprocess
import tempfile
import logging

from mutacc_auto.utils import path_parse


LOG = logging.getLogger(__name__)

#MAKE SBATCH OPTIONS VARIABLE!!!
SBATCH_OPTIONS = {

    '--account': 'account',
    '-n': '1',
    '-t': '5:00:00',
    '-J': 'JOB_NAME',
    '--qos': 'low',
    '-e': "STANDARD_ERROR",
    '-o': "STANDARD_OUT",
    '--mail-type': 'FAIL',
    '--mail-type': 'END',
    '--mail-user': 'USER_EMAIL'

}

def mutacc_slurm_extract(input_file, padding, environment, job_directory, mutacc_conf=None):

    job_directory = path_parse.make_dir(job_directory)

    with tempfile.NamedTemporaryFile(mode = 'w',
                                     suffix = '.sh',
                                     prefix = 'mutacc_extract',
                                     dir = job_directory,
                                     delete = False) as sbatch_script:

        sbatch_script.write("#!/bin/bash\n")

        for key in SBATCH_OPTIONS.keys():

            sbatch_script.write("#SBATCH {}={}\n".format(key, SBATCH_OPTIONS[key]))

        sbatch_script.write("source activate {}\n".format(environment))

        mutacc_command = ['mutacc']

        if mutacc_conf:

            mutacc_command.append('--config-file')
            mutacc_command.append('mutacc_conf')

        mutacc_command.extend(
            [
                'extract',
                '--padding', str(padding),
                '--case', input_file,
            ]
        )


        sbatch_script.write(' '.join(mutacc_command))
        sbatch_script.write("\n")


    print(subprocess.check_output(['cat', sbatch_script.name]).decode("utf-8"))

    #ADD SBATCH COMMAND WITH subprocess
    #subprocess.call([sbatch, sbatch_script.name])


if __name__ == '__main__':

    mutacc_slurm_extract('INPUT.yaml', 300, 'ENVIRONMENT', '~/TEST_MUTACC_AUTO', mutacc_conf='CONFIG.yaml')
