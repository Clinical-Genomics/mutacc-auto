import pytest
from mock import patch, Mock
import unittest
from pathlib import Path
import os

from mutacc_auto.build_input.input_assemble import *

def test_get_case(scout_case):
    bam_file_paths = {
        'ADM1059A2': '/Path/to/ADM1059A2/bam',
        'ADM1059A1': '/Path/to/ADM1059A1/bam',
        'ADM1059A3': '/Path/to/ADM1059A3/bam'
        }
    case_dict = get_case(scout_case, bam_file_paths, '/path/to/vcf')

    assert case_dict['variants'] == '/path/to/vcf'

def test_assemble_samples(scout_case):

    bam_file_paths = {
        'ADM1059A2': '/Path/to/ADM1059A2/bam',
        'ADM1059A1': '/Path/to/ADM1059A1/bam',
        'ADM1059A3': '/Path/to/ADM1059A3/bam'
        }

    individuals = scout_case['individuals']

    samples = assemble_samples(individuals, bam_file_paths)

    assert len(samples) == 3

    bam_file_paths = {
        'ADM1059A2': '/Path/to/ADM1059A2/bam',
        'ADM109A1': '/Path/to/ADM1059A1/bam',
        'ADM1059A3': '/Path/to/ADM1059A3/bam'
        }

    with pytest.raises(NoBamException) as error:

        samples = assemble_samples(individuals, bam_file_paths)
