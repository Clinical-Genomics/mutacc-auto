import pytest
from pathlib import Path
import datetime

from mutacc_auto.files.sbatch import *

def test_SbatchScript(tmpdir):


    tmp_dir = Path(tmpdir.mkdir('test_write_input'))


    with SbatchScript(tmp_dir,
                      'mutacc_env',
                      {'log_directory': tmp_dir, 'email':'email'},
                      'case_id') as sbatch_script:

        sbatch_script.write_section('Command to run')

    sbatch_path = sbatch_script.path

    assert Path(sbatch_path).exists()

    with SbatchScript(tmp_dir,
                     'mutacc_env',
                     {'log_directory': tmp_dir, 'email':'email', 'account':'account'},
                     'case_id',
                     conda=True) as sbatch_script:

        sbatch_script.write_section('Command to run')

    sbatch_path = sbatch_script.path

    assert Path(sbatch_path).exists()
