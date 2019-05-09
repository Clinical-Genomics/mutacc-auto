import logging

from mutacc_auto.commands.mutacc_command import MutaccExport

LOG = logging.getLogger(__name__)


def run_mutacc_export_command(mutacc_config, mutacc_binary=None, case_query=None, variant_query=None,
                              proband=False, member='affected', sample_name=None):

    mutacc_export_command = MutaccExport(config_file=mutacc_config,
                                         mutacc_binary=mutacc_binary,
                                         case_query=case_query,
                                         variant_query=variant_query,
                                         proband=proband,
                                         member=member,
                                         sample_name=sample_name)
    mutacc_export_command.call()

def export_trio(mutacc_config, mutacc_binary=None, case_query=None, variant_query=None):

    for member in ('child', 'father', 'mother'):

        run_mutacc_export_command(mutacc_config=mutacc_config,
                                  mutacc_binary=mutacc_binary,
                                  case_query=case_query,
                                  variant_query=variant_query,
                                  proband=True if member == 'child' else False,
                                  member=member,
                                  sample_name=member)
