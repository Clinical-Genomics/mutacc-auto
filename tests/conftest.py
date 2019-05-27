import pytest
import json
import yaml

HK_OUT_FILE = "tests/fixtures/HK_output_test.txt"
SCOUT_OUT_FILE = "tests/fixtures/scout_output.json"
CASE_YAML = "tests/fixtures/case_input.yaml"
CONFIG = "tests/fixtures/config_file.yaml"
BACKGROUND = "tests/fixtures/background.yaml"

@pytest.fixture
def housekeeper_output():

    with open(HK_OUT_FILE) as hk_handle:

        hk_out = hk_handle.read()

    return hk_out

@pytest.fixture
def case_dict():

    with open(CASE_YAML) as case_handle:

        case = yaml.load(case_handle, Loader=yaml.FullLoader)

    return case

@pytest.fixture
def scout_case():

    with open(SCOUT_OUT_FILE) as case_handle:

        case = yaml.load(case_handle, Loader=yaml.FullLoader)

    return case[0]

@pytest.fixture
def scout_output():

    with open(SCOUT_OUT_FILE) as case_handle:

        case = case_handle.read()

    return case

@pytest.fixture
def configuration_file():

    return CONFIG

@pytest.fixture
def mutacc_export_output():

    mutacc_export_out = '{"vcf_file": "path/to/vcf", "query_file": "path/to/query"}'
    return mutacc_export_out

@pytest.fixture
def mutacc_synthesize_output():

    mutacc_synthesize_out = '{"fastq_files": ["fastq1", "fastq2"]}'
    return mutacc_synthesize_out

@pytest.fixture
def mutacc_synthesize_input():

    synth_input = {'fastq1':'path/to/background_fastq1',
                   'fastq2':'path/to/background_fastq2',
                   'bam':'path/to/background_bam',
                   'query':'path/to/mutacc_query'}

    return synth_input

@pytest.fixture
def background_set():

    backgrounds = {'father': {'fastq1': 'fastq1', 'fastq2': 'fastq2', 'bam': 'bam'},
                   'mother': {'fastq1': 'fastq1', 'fastq2': 'fastq2', 'bam': 'bam'},
                   'child': {'fastq1': 'fastq1', 'fastq2': 'fastq2', 'bam': 'bam'}}
    return backgrounds


@pytest.fixture
def background_file():
    return BACKGROUND
