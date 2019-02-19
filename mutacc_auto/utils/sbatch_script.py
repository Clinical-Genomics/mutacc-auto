import tempfile
import logging
import datetime
import re
from pathlib import Path
from shutil import rmtree

from mutacc_auto.utils import path_parse


LOG = logging.getLogger(__name__)


class SbatchScript():
    """
        Context manager to write sbatch scripts
    """

    def __init__(self, template_file, environment, job_directory, job_name):

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

        self.make_header(template_file, job_name)
        self.make_environment(environment)

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.script_handle.close()

    def make_header(self, template_file, job_name):

        #Matches the -J or --job-name option
        job_option_regexp = re.compile(
                r"((\s)(\-){2}job(\-){1}name[\s\=])|((\s)(\-){1}J[\s\=])"
            )

        with open(template_file, 'r') as template_handle:

            first_line = template_handle.readline()
            if not first_line.startswith('#!'):

                LOG.warning('Please include shebang at first line')
                print("NO SHEBANG")
                raise Exception

            else:
                self.script_handle.write(first_line)

            for line in template_handle.readlines():
                #JOBNAME CAN NOT BE PREDEFINED IN TEMPLATE FILE
                if line.startswith('#') \
                and not job_option_regexp.search(line):
                    self.script_handle.write(line)

        job_name = job_name+str(datetime.datetime.now().timestamp())
        self.script_handle.write("#SBATCH --job-name={}\n\n".format(job_name))

    def make_environment(self, environment):
        self.script_handle.write(
            "source activate {}\n\n".format(environment)
            )

    def write_command(self, command_string):
        self.script_handle.write(command_string)

    @property
    def path(self):

        return self.script_handle.name
