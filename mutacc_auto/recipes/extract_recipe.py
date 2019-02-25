from mutacc_auto.commands.mutacc_command import MutAccExract
from mutacc_auto.commands.sbatch_command import SbatchCommand
from mutacc_auto.files.sbatch import SbatchScript

def write_sbatch_script(tmp_dir,
                        environment,
                        mutacc_extract_command,
                        stdout_file,
                        stderr_file,
                        email,
                        conda=False):

    with SbatchScript(
            environment,
            stdout_file,
            stderr_file,
            email,
            tmp_dir,
            conda=conda
        ) as sbatch_handle:

        sbatch_handle.write_section(mutacc_extract_command)

        sbatch_path = sbatch_handle.path

    return sbatch_path



def get_mutacc_extract_command(mutacc_conf, input_file, padding):

    mutacc_extract_command = MutAccExract(mutacc_conf, padding, input_file)

    return str(mutacc_extract_command)

def sbatch_run(sbatch_script_path, wait=False, dry=False):

    sbatch_command = SbatchCommand(sbatch_script_path, wait=wait)

    if not dry:
        sbatch_command.call()
    else:
        print('Command: ', sbatch_command)


def run_mutacc_extract(tmp_dir,
                       mutacc_conf,
                       input_file,
                       padding,
                       environment,
                       stdout_file,
                       stderr_file,
                       email,
                       conda=False,
                       wait=False,
                       dry=False):

    mutacc_extract_command = get_mutacc_extract_command(mutacc_conf, input_file, padding)

    sbatch_script_path = write_sbatch_script(tmp_dir,
                                             environment,
                                             mutacc_extract_command,
                                             stdout_file,
                                             stderr_file,
                                             email)

    sbatch_run(sbatch_script_path, wait, dry=dry)
