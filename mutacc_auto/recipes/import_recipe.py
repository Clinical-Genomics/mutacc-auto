from mutacc_auto.commands.mutacc_command import MutaccImport

def import_extracted_case(extracted_case_file, config_file):

    mutacc_import_command = MutaccImport(config_file, extracted_case_file)
    mutacc_import_command.call()
