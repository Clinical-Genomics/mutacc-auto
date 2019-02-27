import pytest
from pathlib import Path
import datetime

from mutacc_auto.files.sbatch import *

def test_SbatchScript(tmpdir):


    tmp_dir = Path(tmpdir.mkdir('test_write_input'))


    sbatch_script = SbatchScript('mutacc_env','stdout_file','stderr_file','email',
                                 tmp_dir)

    sbatch_script.write_section('Command to run')

    sbatch_path = sbatch_script.path

    assert Path(sbatch_path).exists()

    sbatch_script = SbatchScript('mutacc_env','stdout_file','stderr_file','email',
                                 tmp_dir, conda=True)

    sbatch_script.write_section('Command to run')

    sbatch_path = sbatch_script.path

    assert Path(sbatch_path).exists()

def test_get_timestamp():

    timestamp = datetime.datetime.fromtimestamp(float(get_timestamp()))
    today = datetime.date.today()
    assert timestamp.day == today.day
    assert timestamp.month == today.month
