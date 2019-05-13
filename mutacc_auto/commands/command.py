
import subprocess
import logging
import time

LOG = logging.getLogger(__name__)

SECONDS_BETWEEN_CALLS = 0.5

class Command():

    """
        Class to specify commands and to run them using the
        subprocess module in python
    """

    def __init__(self, base_command):

        """
            Args:
                base_command(str): base_command
        """
        #initiate command list
        self.command = [base_command]


    def __str__(self):

        return ' '.join(self.command)

    def add_subcommand(self, subcommand):

        self.command.append(subcommand)

    def add_argument(self, argument):

        self.command.append(argument)

    def add_option(self, option, value = None, long = True):

        option_str = "-"

        if long:

            option_str += "-"

        option_str += option

        self.command.append(option_str)

        if value:

            self.command.append(str(value))

    def check_output(self):

        """
            Returns the stdout of the command
        """
        time.sleep(SECONDS_BETWEEN_CALLS)
        try:

            command_stdout = subprocess.check_output(self.command)

        except (OSError, subprocess.CalledProcessError):

            LOG.critical("Could not run command: {}".format(
                    str(self)
                )
            )

            raise

        command_stdout = command_stdout.decode('utf-8')

        LOG.debug("Executed: {}".format(str(self)))

        return command_stdout

    def call(self):

        """
            Calls the command
        """
        time.sleep(SECONDS_BETWEEN_CALLS)
        try:

            result = subprocess.check_call(self.command)

        except (OSError, subprocess.CalledProcessError):

            LOG.critical("Could not run command: {}".format(
                    str(self)
                )
            )

            raise

        LOG.debug("Executed: {}".format(str(self)))

        return result
