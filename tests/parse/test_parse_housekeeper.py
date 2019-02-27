import pytest

from mutacc_auto.parse.parse_housekeeper import *

def test_get_bams_from_housekeeper(housekeeper_output):

    bam_files = get_bams_from_housekeeper(housekeeper_output)

    assert type(bam_files) == dict
    assert len(bam_files) == 3

    for sample in bam_files:

        assert bam_files[sample].endswith('bam')
