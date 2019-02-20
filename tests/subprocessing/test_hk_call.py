import pytest
from mutacc_auto.subprocessing import hk_call

def test_find_bams():

    bams = hk_call.find_bams('case')

    assert len(bams) == 3

    for key in bams.keys():
        assert bams[key].endswith('bam')
