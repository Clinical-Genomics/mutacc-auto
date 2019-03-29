import pytest
from mock import patch


from mutacc_auto.commands.command import Command
from mutacc_auto.commands.sbatch_command import SbatchCommand
from mutacc_auto.commands.scout_command import ScoutExportCases, ScoutExportCausativeVariants
from mutacc_auto.commands.housekeeper_command import HousekeeperCommand

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

def test_ScoutExportCases():

    command = ScoutExportCases()

    assert str(command) == "scout export cases --json --finished"

    command = ScoutExportCases(config_file='config_file')

    assert str(command) == "scout --config config_file export cases --json --finished"

def test_ScoutExportCausativeVariants():

    command = ScoutExportCausativeVariants(case_id='case_id',config_file='config_file')

    assert str(command) == "scout --config config_file export variants --json --case-id case_id"

def test_HousekeeperCommand():

    command = HousekeeperCommand(case_id='case_id', config_file='config_file')

    assert str(command) == "housekeeper --config config_file get -V case_id"
