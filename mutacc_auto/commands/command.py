
import subprocess
import logging

LOG = logging.getLogger(__name__)

class Command():

    """
        Class to specify command line arguments and to run them using the
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

        try:

            command_stdout = subprocess.check_output(self.command)

        except (OSError, subprocess.CalledProcessError):

            LOG.critical("Could not run command: {}".format(
                    str(self)
                )
            )

            raise

        command_stdout = command_stdout.decode('utf-8')

        LOG.debug("Executed:".format(str(self)))

        return command_stdout

    def call(self):

        try:

            subprocess.check_call(self.command)

        except (OSError, subprocess.CalledProcessError):

            LOG.critical("Could not run command: {}".format(
                    str(self)
                )
            )

            raise

        LOG.debug("Executed:".format(str(self)))

if __name__ == '__main__':

    command = Command('ls')
    command.add_option('l', long = False)
    command.add_option('a', long = False)
    command.add_argument('/Users/')
    print(command)
    print(command.command)
    print(command.check_output())
