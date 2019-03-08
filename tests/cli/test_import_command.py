import pytest
from mock import patch
import yaml
from pathlib import Path

from click.testing import CliRunner

from mutacc_auto.cli.root import cli

INPUTS_LIST = [{'input_file': 'path_to_file', 'padding':600}]*2
SBATCH_TEMPLATE = "tests/fixtures/sbatch_template.txt"

TMP_DIR_NAME = 'test_import_command'
CONF_FILE_NAME = 'tmp_conf.yaml'
IMPORT_FILE_NAME = 'tmp_test.mutacc'

@patch('mutacc_auto.cli.import_command.import_extracted_case')
def test_import_command(
        mock_import,
        tmpdir
    ):

    tmp_dir = Path(tmpdir.mkdir(TMP_DIR_NAME))

    with open(tmp_dir.joinpath(CONF_FILE_NAME), 'w') as conf_handle:

        conf_dict = {'case_dir': str(tmp_dir)}
        yaml.dump(conf_dict, conf_handle)
        conf_path = conf_handle.name

    with open(tmp_dir.joinpath(IMPORT_FILE_NAME), 'w') as handle:
        handle.write('\n')

    runner = CliRunner()
    result = runner.invoke(cli, [
            'import',
            '--config-file', conf_path,
            '--dry',
            '--verbose'
        ]
    )

    assert result.exit_code == 0

    result = runner.invoke(cli, [
            'import',
            '--config-file', conf_path,
        ]
    )

    assert result.exit_code == 0

    mock_import.assert_called_with(
                str(tmp_dir.joinpath(IMPORT_FILE_NAME)),
                conf_path
            )
