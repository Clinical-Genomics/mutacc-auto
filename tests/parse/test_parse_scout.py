import pytest
from copy import deepcopy
import json

from mutacc_auto.parse.parse_scout import (get_cases_from_scout, NoCausativesException)

def test_get_cases_from_scout(scout_output):

    cases = get_cases_from_scout(scout_output)

    assert len(cases) == 1
    assert type(cases) == list
    assert type(cases[0]) == dict
    assert set(cases[0].keys()).issuperset(set(['individuals', 'display_name']))

    cases = get_cases_from_scout(scout_output, days_ago=20000)

    len(cases) == 1

    cases = get_cases_from_scout(scout_output, days_ago=1)

    len(cases) == 0
    type(cases) == list

    #Remove 'causatives from scout output'
    no_causatives = json.loads(scout_output)
    for case in no_causatives:
        case.pop('causatives')
    no_causatives=json.dumps(no_causatives)

    with pytest.raises(NoCausativesException):

        cases = get_cases_from_scout(no_causatives)
