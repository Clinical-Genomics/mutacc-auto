import pytest
from mock import patch
import yaml
from pathlib import Path

from click.testing import CliRunner

from mutacc_auto.cli.root import cli

INPUTS_LIST = [{'input_file': 'path_to_file', 'padding':600}]*2

@patch('mutacc_auto.cli.import_command.get_inputs')
@patch('mutacc_auto.cli.import_command.run_mutacc_extract')
@patch('mutacc_auto.cli.import_command.import_extracted_case')
def test_import_command(
        mock_import,
        mock_extract,
        mock_inputs,
        tmpdir
    ):

    tmp_dir = Path(tmpdir.mkdir('test_import_command'))
    mock_inputs.return_value = INPUTS_LIST

    with open(tmp_dir.joinpath('tmp_conf.yaml'), 'w') as conf_handle:

        conf_dict = {'case_dir': str(tmp_dir)}
        yaml.dump(conf_dict, conf_handle)
        conf_path = conf_handle.name

    with open(tmp_dir.joinpath('tmp_test.mutacc'), 'w') as handle:
        handle.write('\n')

    runner = CliRunner()
    result = runner.invoke(cli, [
            'import',
            '--case-id', 'test_id',
            '--environment', 'env',
            '--conf-file', conf_path,
            '--dry'
        ]
    )

    assert result.exit_code == 0
    
