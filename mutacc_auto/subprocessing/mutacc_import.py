
import subprocess
import logging


LOG = logging.getLogger(__name__)

def mutacc_import(case_file, config_file):

    mutacc_command = [
                'mutacc',
                '--config-file',
                config_file,
                'db',
                'import',
                case_file
                ]

    try:
        subprocess.check_call(mutacc_command)
    except (OSError, subprocess.CalledProcessError):
        LOG.critical("Could not run command {}".format(' '.join(mutacc_command)))
