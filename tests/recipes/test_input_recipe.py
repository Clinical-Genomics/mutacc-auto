import pytest
from mutacc_auto.recipes.input_recipe import get_bams, get_cases, write_vcf, write_input, get_analysis_type, get_inputs

from mutacc_auto.commands.command import Command

from mock import patch, Mock
import unittest
from pathlib import Path
import os

HK_OUT_FILE = "tests/fixtures/HK_output_test.txt"
SCOUT_OUT_FILE = "tests/fixtures/scout_output.json"
TEST_VCF = "tests/fixtures/test_vcf.vcf"

def mock_hk_output(case_id):

    with open(HK_OUT_FILE) as hk_handle:

        hk_out = hk_handle.read()

    return hk_out

def mock_scout_output(case_id):

    with open(SCOUT_OUT_FILE) as scout_handle:

        scout_out = scout_handle.read()

    return scout_out

def mock_vcf(case_id):

    with open(TEST_VCF) as vcf_handle:

        vcf_out = vcf_handle.read()

    return vcf_out

@patch.object(Command, 'check_output', mock_scout_output)
def test_get_cases():
    cases = get_cases(case_id='case_id')

    assert len(cases)==1
    assert cases[0]['display_name'] == '643594'

@patch.object(Command, 'check_output', mock_hk_output)
def test_get_bams():
    bams = get_bams('case_id')

    assert len(bams) == 3

@patch.object(Command, 'check_output', mock_vcf)
def test_write_vcf(tmpdir):
    tmp_dir = Path(tmpdir.mkdir('test_write_vcf'))
    vcf_path = write_vcf('case_id', tmp_dir)

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

@patch('mutacc_auto.recipes.input_recipe.get_cases')
@patch('mutacc_auto.recipes.input_recipe.get_bams')
@patch('mutacc_auto.recipes.input_recipe.write_vcf')
def test_get_inputs(mock_write_vcf, mock_get_bams, mock_get_cases, tmpdir, scout_case):

    tmp_dir = Path(tmpdir.mkdir('test_get_inputs'))
    mock_get_cases.return_value = [scout_case]*2
    mock_get_bams.return_value = {
        'ADM1059A2': '/Path/to/ADM1059A2/bam',
        'ADM1059A1': '/Path/to/ADM1059A1/bam',
        'ADM1059A3': '/Path/to/ADM1059A3/bam'
        }
    mock_write_vcf.return_value = '/path/to/vcf'

    inputs = get_inputs(tmp_dir, days_ago = 1234)

    mock_get_cases.assert_called_with(None,1234)
    mock_get_bams.assert_called_with('643594')
    mock_write_vcf.assert_called_with('643594', tmp_dir)

    assert len(inputs) == 2

    for input in inputs:
        assert input['padding'] == 0
        assert os.path.isfile(input['input_file'])

    with patch("mutacc_auto.recipes.input_recipe.get_analysis_type", return_value = 'wgs') as mock_analysis:

        inputs = get_inputs(tmp_dir, case_id = 'case_id', padding = 300)

        for input in inputs:
            assert input['padding'] == 300
            assert os.path.isfile(input['input_file'])
