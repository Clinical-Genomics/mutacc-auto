
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
ACCOUNT = 'cust000'
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

        header = ""
        for option in HEADER_OPTIONS:
            header += f"{HEADER_PREFIX} {option[0]}{option[2]}{option[1]}\n"

        header += f"{HEADER_PREFIX} -e {stderr_file}\n"
        header += f"{HEADER_PREFIX} -o {stdout_file}\n"
        header += f"{HEADER_PREFIX} --mail-user={email}\n"

        return header

    @staticmethod
    def get_environment(environment, conda = False):

        if conda:
            return f"conda activate {environment}\n"

        return f"source activate {environment}"

    @staticmethod
    def get_shebang():

        return SHEBANG


    def __init__(self, environment, stdout_file, stderr_file, email, job_directory, conda = False):

        """
            Args:
                template_file(str): path to file containing the headers to
                                    be included.
                environment(str): environment to be used
                job_directory(Path): directory to store sbatch script
                job_name(str): name of job
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

        return self.script_handle.name

if __name__ == '__main__':

    tmp_dir = Path(tempfile.mkdtemp())

    with SbatchScript('mutacc_env', 'std_out', 'std_err', 'EMAIL', tmp_dir, conda=True) as sbatch_handle:

        sbatch_handle.write_section("COMMAND DSADSA dsa")

    print(sbatch_handle.path)
    sbatch_handle.delete_file()
