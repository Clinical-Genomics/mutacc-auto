from .command import Command as BaseCommand

BGZIP_COMMAND = 'bgzip'
TABIX_COMMAND = 'tabix'
BCFTOOLS_MERGE_COMMAND = 'bcftools'

class BgzipCommand(BaseCommand):

    def __init__(self, vcf_file):

        super(BgzipCommand, self).__init__(BGZIP_COMMAND)

        self.add_argument(vcf_file)

class TabixCommand(BaseCommand):

    def __init__(self, vcf_file):

        super(TabixCommand, self).__init__(TABIX_COMMAND)

        self.add_argument(vcf_file)

class BcftoolsMergeCommand(BaseCommand):

    def __init__(self, vcf_files, out_vcf=None):

        super(BcftoolsMergeCommand, self).__init__(BCFTOOLS_MERGE_COMMAND)

        self.add_subcommand('merge')

        if out_vcf:
            self.add_option('output', out_vcf)

        self.add_option('output-type', 'z')

        for vcf_file in vcf_files:
            self.add_argument(vcf_file)
