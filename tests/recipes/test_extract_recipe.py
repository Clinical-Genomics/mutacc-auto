import pytest
from pathlib import Path
import os
from mock import patch

from mutacc_auto.recipes.extract_recipe import *
from mutacc_auto.commands.command import Command

def test_write_sbatch_script(tmpdir):

    tmp_dir = Path(tmpdir.mkdir('test_write_sbatch_script'))

    sbatch_path = write_sbatch_script(tmp_dir,
                                      'environment',
                                      'mutacc extract ...',
                                      {'log_directory': tmp_dir, 'email': 'email'},
                                      'case_id')

    assert os.path.isfile(sbatch_path)

def test_get_mutacc_extract_command():

    mutacc_extract_command = MutaccExtract('mutacc_conf', 699, 'input_file')
    true_command = "mutacc --config-file mutacc_conf extract --padding 699 --case input_file"
    assert str(mutacc_extract_command) == true_command

@patch.object(Command, 'call')
def test_sbatch_run(command):

    sbatch_run('/sbatch/script/path', dry=True)
    sbatch_run('/sbatch/script/path')

@patch('mutacc_auto.recipes.extract_recipe.sbatch_run')
def test_run_mutacc_extract(mock_sbatch_run, tmpdir):

    tmp_dir = Path(tmpdir.mkdir('test_run_mutacc_extract'))

    run_mutacc_extract(
        tmp_dir,
        'config',
        'input_file',
        123,
        'case_id',
        'env',
        {'log_directory': tmp_dir, 'email': 'email'},
    )
