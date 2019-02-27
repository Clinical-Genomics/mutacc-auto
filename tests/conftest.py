import pytest
import json
import yaml

HK_OUT_FILE = "tests/fixtures/HK_output_test.txt"
SCOUT_OUT_FILE = "tests/fixtures/scout_output.json"
CASE_YAML = "tests/fixtures/case_input.yaml"

@pytest.fixture
def housekeeper_output():

    with open(HK_OUT_FILE) as hk_handle:

        hk_out = hk_handle.read()

    return hk_out

@pytest.fixture
def case_dict():

    with open(CASE_YAML) as case_handle:

        case = yaml.load(case_handle)

    return case

@pytest.fixture
def scout_case():

    with open(SCOUT_OUT_FILE) as case_handle:

        case = yaml.load(case_handle)

    return case[0]

@pytest.fixture
def scout_output():

    with open(SCOUT_OUT_FILE) as case_handle:

        case = case_handle.read()

    return case
