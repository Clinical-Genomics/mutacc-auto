from .command import Command as BaseCommand

BASE_COMMAND = "sbatch"

class SbatchCommand(BaseCommand):

    def __init__(self, sbatch_script_path):

        super(SbatchCommand,self).__init__(BASE_COMMAND)

        self.add_argument(sbatch_script_path)
