
from .command import Command as BaseCommand

BASE_COMMAND = "mutacc"


#Inherit from BaseCommand
class MutaccCommand(BaseCommand):

    def __init__(self, config_file, mutacc_binary=None):

        super(MutaccCommand, self).__init__(BASE_COMMAND)

        self.command = [BASE_COMMAND]
        if mutacc_binary:
            self.command = [mutacc_binary]

        self.add_option('config-file', value=config_file)

class MutaccExtract(MutaccCommand):

    def __init__(self, config_file, padding, case_file, mutacc_binary=None):

        super(MutaccExtract, self).__init__(config_file, mutacc_binary=mutacc_binary)

        self.add_subcommand('extract')
        self.add_option('padding', value=str(padding))
        self.add_option('case', value=str(case_file))


class MutaccImport(MutaccCommand):

    def __init__(self, config_file, extracted_case_file, mutacc_binary=None):

        super(MutaccImport, self).__init__(config_file, mutacc_binary=mutacc_binary)

        self.add_subcommand('db')
        self.add_subcommand('import')
        self.add_argument(str(extracted_case_file))

class MutaccExport(MutaccCommand):

    def __init__(self, config_file, mutacc_binary=None,
                 proband=False, member='affected', sample_name=None):

        super(MutaccExport, self).__init__(config_file, mutacc_binary=mutacc_binary)

        self.add_subcommand('db')
        self.add_subcommand('export')

        if sample_name is not None:
            self.add_option('sample-name', sample_name)
        if proband:
            self.add_option('proband')

        self.add_option('member', member)
        self.add_option('all-variants')
        self.add_option('json-out')

class MutaccSynthesize(MutaccCommand):

    def __init__(self, config_file, fastq1, bam_file, query_file, sample_dir=None,
                 fastq2=None, mutacc_binary=None):

        super(MutaccSynthesize, self).__init__(config_file, mutacc_binary=mutacc_binary)

        self.add_subcommand('synthesize')

        self.add_option('background-bam', bam_file)
        self.add_option('background-fastq', fastq1)
        if fastq2 is not None:
            self.add_option('background-fastq2', fastq2)
        self.add_option('query', query_file)
        if sample_dir is not None:
            self.add_option('dataset-dir', sample_dir)
        self.add_option('json-out')
