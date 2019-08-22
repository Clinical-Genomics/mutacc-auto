import pytest
from mutacc_auto.recipes.input_recipe import write_vcf, write_input, get_analysis_type, get_input

from mutacc_auto.commands.command import Command

from mock import patch, Mock
import unittest
from pathlib import Path
import os

HK_OUT_FILE = "tests/fixtures/HK_output_test.txt"
SCOUT_OUT_FILE = "tests/fixtures/scout_output.json"
TEST_VCF = "tests/fixtures/test_vcf.vcf"
TEST_SCOUT_VARIANT = "tests/fixtures/scout_variant_output.json"

def mock_hk_output():

    with open(HK_OUT_FILE) as hk_handle:

        hk_out = hk_handle.read()

    return hk_out

def mock_scout_output():

    with open(SCOUT_OUT_FILE) as scout_handle:

        scout_out = scout_handle.read()

    return scout_out

def mock_scout_variant():

    with open(TEST_SCOUT_VARIANT) as vcf_handle:

        vcf_out = vcf_handle.read()

    return vcf_out


def test_write_vcf(tmpdir):
    tmp_dir = Path(tmpdir.mkdir('test_write_vcf'))
    vcf_path = write_vcf(tmp_dir, mock_scout_variant(), 'case_id')

    assert os.path.isfile(vcf_path)

def test_write_input(tmpdir, case_dict):
    tmp_dir = Path(tmpdir.mkdir('test_write_input'))
    input_path = write_input(case_dict, tmp_dir)

    assert os.path.isfile(input_path)

def test_get_analysis_type(scout_case):

    analysis_type = get_analysis_type(scout_case)

    assert analysis_type == 'wes'

    for i in range(len(scout_case['individuals'])):

        scout_case['individuals'][i]['analysis_type'] = 'wgs'

    analysis_type = get_analysis_type(scout_case)

    assert analysis_type == 'wgs'


@patch('mutacc_auto.recipes.input_recipe.write_vcf')
def test_get_input(mock_write_vcf, tmpdir, scout_case, scout_variant_output):

    tmp_dir = Path(tmpdir.mkdir('test_get_inputs'))
    mock_write_vcf.return_value = '/path/to/vcf'

    input = get_input(tmp_dir, scout_case, scout_variant_output, 100)

    mock_write_vcf.assert_called_with(tmp_dir, scout_variant_output, scout_case['_id'])

    assert input['padding'] == 0
    assert os.path.isfile(input['input_file'])

    with patch("mutacc_auto.recipes.input_recipe.get_analysis_type", return_value = 'wgs') as mock_analysis:

        input = get_input(tmp_dir, case_id = 'case_id', padding = 300)

        assert input['padding'] == 300
        assert os.path.isfile(input['input_file'])
