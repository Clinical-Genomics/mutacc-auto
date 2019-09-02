import pytest
from mock import patch


from mutacc_auto.commands.command import Command
from mutacc_auto.commands.sbatch_command import SbatchCommand
from mutacc_auto.commands.mutacc_command import (MutaccExtract, MutaccImport, MutaccExport, MutaccSynthesize)

def test_Command():

    command = Command('ls')
    command.add_option('l', long=False)

    output = command.check_output()

    assert type(output) == str

    result = command.call()

    assert result == 0

    command = Command('loij438hss')

    #Check that errors are raised if the command
    #is faulty
    with pytest.raises(OSError) as error:

        output = command.check_output()

    with pytest.raises(OSError) as error:

        command.call()

def test_SbatchCommand():

    command = SbatchCommand('script')

    assert str(command) == "sbatch script"


def test_MutaccExtract():

    command = MutaccExtract('config_file', 300, 'case.yaml', mutacc_binary='/path/to/mutacc')

    assert str(command) == "/path/to/mutacc --config-file config_file extract --padding 300 --case case.yaml"

    command = MutaccExtract('config_file', 300, 'case.yaml')

    assert str(command) == "mutacc --config-file config_file extract --padding 300 --case case.yaml"

def test_MutaccImport():

    command = MutaccImport('config_file', 'case', mutacc_binary='/path/to/mutacc')

    assert str(command) == "/path/to/mutacc --config-file config_file db import case"

    command = MutaccImport('config_file', 'case')

    assert str(command) == "mutacc --config-file config_file db import case"

def test_MutaccExport():

    command = MutaccExport(config_file='config_file',
                           mutacc_binary='path/to/mutacc',
                           proband=True,
                           member='child',
                           sample_name='sample')

    assert str(command) == ("path/to/mutacc --config-file config_file db export "
                            "--sample-name sample "
                            "--proband --member child --all-variants --json-out")
