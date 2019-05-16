import pytest
from mock import patch
import yaml

from click.testing import CliRunner

from mutacc_auto.cli.root import cli

@patch('mutacc_auto.cli.export_command.export_dataset')
def test_export_command(mock_export_dataset,
                        configuration_file,
                        background_file):
    mock_export_dataset = {}
    runner = CliRunner()
    result = runner.invoke(cli, ['--config-file', configuration_file,
                                 'export',
                                 '-o', 'vcf_out',
                                 '-b', background_file])
    #mock_mkdir.assert_called_with('dsa')
    assert result.exit_code == 0
