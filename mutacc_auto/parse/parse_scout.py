import json
from datetime import datetime, timedelta

from mutacc_auto.commands.scout_command import ScoutExportCases

#The timestamp in the scout database seems to be given with
#millisecond precision, it is therefor necessary to divide the
#timestamp with 1000 to make it compatible with the timestamp from
#the datetime module
TIMESTAMP_DIVIDE = 1000.0


def get_cases_from_scout(scout_output, days_ago=None):

    """
        Parses the scout output

        Args:
            scout_output (str): output from scout command
            days_ago (int): number of days since case updated

        Returns (list(dict)): list of dictionaries representing the cases 
    """

    cases = json.loads(scout_output)

    if not days_ago:
        return cases

    #MAKE DATETIME OBJECT days DAYS ago
    days_datetime = datetime.now() - timedelta(days=days_ago)

    recent_cases = []

    for case in cases:
        case_date = case['updated_at']['$date']
        case_date = datetime.fromtimestamp(case_date/TIMESTAMP_DIVIDE)
        if case_date > days_datetime:
            recent_cases.append(case)

    return recent_cases
