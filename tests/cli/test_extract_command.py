import pytest
from mock import patch
import yaml
from pathlib import Path

from click.testing import CliRunner

from mutacc_auto.cli.root import cli

INPUTS_LIST = [{'input_file': 'tests/fixtures/case_input.yaml', 'padding':600}]*2
SBATCH_TEMPLATE = "tests/fixtures/sbatch_template.txt"

@patch('mutacc_auto.cli.extract_command.get_inputs')
@patch('mutacc_auto.cli.extract_command.run_mutacc_extract')
def test_extract_command(
        mock_extract,
        mock_inputs,
        configuration_file,
        tmpdir
    ):

    tmp_dir = Path(tmpdir.mkdir('test_export_command'))
    mock_inputs.return_value = INPUTS_LIST
    mock_extract.return_value = SBATCH_TEMPLATE

    with open(tmp_dir.joinpath('tmp_conf.yaml'), 'w') as conf_handle:

        conf_dict = {'case_dir': str(tmp_dir)}
        yaml.dump(conf_dict, conf_handle)
        conf_path = conf_handle.name

    with open(tmp_dir.joinpath('tmp_test.mutacc'), 'w') as handle:
        handle.write('\n')

    runner = CliRunner()
    result = runner.invoke(cli, [
            '--config-file', configuration_file,
            'extract',
            '--case-id', 'test_id',
            '--environment', 'env',
            '--mutacc-config', conf_path,
            '--log-directory', str(tmp_dir),
            '--email', 'email@email.com',
            '--dry',
            '--verbose'
        ]
    )

    assert result.exit_code == 0

    result = runner.invoke(cli, [
            'extract',
            '--days-ago', '300',
            '--environment', 'env',
            '--mutacc-config', conf_path,
            '--log-directory', tmp_dir
        ]
    )

    assert result.exit_code == 0
