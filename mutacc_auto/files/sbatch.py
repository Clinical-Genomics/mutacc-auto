
import datetime
import logging
import re
from pathlib import Path
from shutil import rmtree
import tempfile


def get_timestamp():

    return str(datetime.datetime.now().timestamp())

LOG = logging.getLogger(__name__)

SHEBANG = '#! /bin/bash -l'

HEADER_PREFIX = '#SBATCH'

JOBNAME = 'mutacc_' + get_timestamp()
ACCOUNT = 'prod001'
NODES = '1'
TIME = '4:00:00'
PRIORITY = 'low'
MAIL_FAIL = 'FAIL'
MAIL_END = 'END'

#SOME CONSTAN SBATCH
# (OPTION, VALUE, SEPARATOR)
HEADER_OPTIONS = (
    ('-A', ACCOUNT, ' '),
    ('-n', NODES, ' '),
    ('-t', TIME, ' '),
    ('-J', JOBNAME, ' '),
    ('--qos', PRIORITY, '='),
    ('--mail-type', MAIL_FAIL, '=' ),
    ('--mail-type', MAIL_END, '=' )
)

class SbatchScript():
    """
        Context manager to write sbatch scripts
    """

    @staticmethod
    def get_header(stdout_file, stderr_file, email):

        """
            Returns header to be printed in sbatch scripts

            Args:
                stdout_file (str): path to file where stdout is written
                stderr_file (str): path to file where stderr is written
                email (str): email to notify if job fails, or completes

            Returns:
                header (str): string with header, lines separated by newline
        """

        header = ""
        #write all constant header options
        for option in HEADER_OPTIONS:
            header += f"{HEADER_PREFIX} {option[0]}{option[2]}{option[1]}\n"
        #write all variable header options
        header += f"{HEADER_PREFIX} -e {stderr_file}\n"
        header += f"{HEADER_PREFIX} -o {stdout_file}\n"
        header += f"{HEADER_PREFIX} --mail-user={email}\n"

        return header

    @staticmethod
    def get_environment(environment, conda = False):

        """
            get command to run the correct environment
        """
        if conda:
            return f"conda activate {environment}\n"

        return f"source activate {environment}"

    @staticmethod
    def get_shebang():

        """
            Returns the shebang line
        """

        return SHEBANG


    def __init__(self, environment, stdout_file, stderr_file, email, job_directory, conda = False):

        """
            Args:

                environment (str): environment to be used
                stdout_file (str)
                stderr_file (str)
                email (str)
                job_directory (str): directory where sbatch script is written
        """

        self.script_handle = tempfile.NamedTemporaryFile(
                                        mode = 'w',
                                        dir = job_directory,
                                        delete = False
                                        )
        self.shebang = self.get_shebang()
        self.header = self.get_header(stdout_file,stderr_file,email)
        self.environment = self.get_environment(environment, conda)

        self.write_section(self.shebang)
        self.write_section(self.header)
        self.write_section(self.environment)

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.script_handle.close()

    def write_section(self, section):
        self.script_handle.write(section+'\n')


    @property
    def path(self):
        """
            Returns path to sbatch script
        """
        return self.script_handle.name
