#!/usr/bin/env python3

import yaml
import sys
from pathlib import Path
import logging
from copy import deepcopy

LOG = logging.getLogger(__name__)

def get_case(case, vcf_file_path):

    case_obj = deepcopy(case)
    samples_obj = case_obj.pop('samples')

    for sample in samples_obj:
        if sample.get('father', None) is None:
            sample['father'] = '0'
        if sample.get('mother', None) is None:
            sample['mother'] = '0'

    return {
        'case': case_obj,
        'samples': samples_obj,
        'variants': vcf_file_path
    }
