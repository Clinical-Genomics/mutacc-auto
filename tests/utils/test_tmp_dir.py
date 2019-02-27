import pytest
from pathlib import Path
from shutil import rmtree

from mutacc_auto.utils.tmp_dir import TemporaryDirectory

def test_TemporaryDirectory():

    with TemporaryDirectory() as tmp_dir:

        assert Path(tmp_dir).exists()
        assert Path(tmp_dir).is_dir()

    assert not Path(tmp_dir).exists()

    with TemporaryDirectory(delete_dir=False) as tmp_dir:

        assert Path(tmp_dir).exists()
        assert Path(tmp_dir).is_dir()

    assert Path(tmp_dir).exists()
    rmtree(tmp_dir)
    
