
from .command import Command as BaseCommand

BASE_COMMAND = "scout"


#Inherit from BaseCommand
class ScoutCommand(BaseCommand):

    def __init__(self):

        super(ScoutCommand, self).__init__(BASE_COMMAND)


class ScoutExportCases(ScoutCommand):

    def __init__(self, case_id=None, config_file=None, scout_binary=None):

        super(ScoutExportCases, self).__init__()

        if scout_binary:
            self.command = [scout_binary]

        if config_file:

            self.add_option('config', value=str(config_file))

        self.add_subcommand('export')
        self.add_subcommand('cases')
        self.add_option('json')

        if case_id:
            self.add_option('case-id', value=case_id)
        else:
            self.add_option('finished')

class ScoutExportCausativeVariants(ScoutCommand):

    def __init__(self, case_id, json_output = True, config_file=None, scout_binary=None):

        super(ScoutExportCausativeVariants, self).__init__()
        
        if scout_binary:
            self.command = [scout_binary]

        if config_file:

            self.add_option('config', value=str(config_file))

        self.add_subcommand('export')
        self.add_subcommand('variants')

        if json_output: self.add_option('json')

        self.add_option('case-id', value=case_id)
