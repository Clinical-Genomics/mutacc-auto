import pytest
from pathlib import Path
import os

from mutacc_auto.build_input.input_assemble import *

def test_get_case(scout_case):

    case_dict = get_case(scout_case, '/path/to/vcf')

    assert case_dict['variants'] == '/path/to/vcf'

def test_assemble_samples(scout_case):

    individuals = scout_case['individuals']

    samples = assemble_samples(individuals)

    assert len(samples) == 3
