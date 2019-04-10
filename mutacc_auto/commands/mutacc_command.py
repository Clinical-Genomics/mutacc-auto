
from .command import Command as BaseCommand

BASE_COMMAND = "mutacc"


#Inherit from BaseCommand
class MutaccCommand(BaseCommand):

    def __init__(self, config_file, mutacc_binary=None):

        super(MutaccCommand, self).__init__(BASE_COMMAND)

        if mutacc_binary:
            self.command = [mutacc_binary]

        self.add_option('config-file', value=config_file)

class MutAccExract(MutaccCommand):

    def __init__(self, config_file, padding, case_file, mutacc_binary=None):

        super(MutAccExract, self).__init__(config_file)

        if mutacc_binary:
            self.command = [mutacc_binary]

        self.add_subcommand('extract')
        self.add_option('padding', value=str(padding))
        self.add_option('case', value=str(case_file))


class MutaccImport(MutaccCommand):

    def __init__(self, config_file, extracted_case_file, mutacc_binary=None):

        super(MutaccImport, self).__init__(config_file)

        if mutacc_binary:
            self.command = [mutacc_binary]

        self.add_subcommand('db')
        self.add_subcommand('import')
        self.add_argument(str(extracted_case_file))
