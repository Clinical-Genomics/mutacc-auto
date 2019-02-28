import pytest
from mock import patch


from mutacc_auto.commands.command import Command
from mutacc_auto.commands.sbatch_command import SbatchCommand
from mutacc_auto.commands.scout_command import ScoutExportCases, ScoutExportCausativeVariants

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

    command = SbatchCommand('script', wait = True)

    assert str(command) == "sbatch --wait script"

def test_ScoutExportCases():

    command = ScoutExportCases()

    assert str(command) == "scout export cases --json --finished"
