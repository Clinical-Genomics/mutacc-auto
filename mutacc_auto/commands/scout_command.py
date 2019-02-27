
from .command import Command as BaseCommand

BASE_COMMAND = "scout"


#Inherit from BaseCommand
class ScoutCommand(BaseCommand):

    def __init__(self):

        super(ScoutCommand, self).__init__(BASE_COMMAND)


class ScoutExportCases(ScoutCommand):

    def __init__(self, case_id=None):

        super(ScoutExportCases, self).__init__()

        self.add_subcommand('export')
        self.add_subcommand('cases')
        self.add_option('json')

        if case_id:
            self.add_option('case-id', value=case_id)
        else:
            self.add_option('finished')

class ScoutExportCausativeVariants(ScoutCommand):

    def __init__(self, case_id):

        super(ScoutExportCausativeVariants, self).__init__()

        self.add_subcommand('export')
        self.add_subcommand('variants')
        self.add_option('case-id', value=case_id)
