import json
from datetime import datetime, timedelta

from mutacc_auto.commands.scout_command import ScoutExportCases

def get_cases_from_scout(scout_output, days_ago=None):

    cases = json.loads(scout_output)

    if not days_ago:
        return cases

    #MAKE DATETIME OBJECT days DAYS ago
    days_datetime = datetime.now() - timedelta(days=days_ago)

    recent_cases = []

    for case in cases:
        case_date = case['updated_at']['$date']
        case_date = datetime.fromtimestamp(case_date/1000.0)
        if case_date > days_datetime:
            recent_cases.append(case)

    return recent_cases


if __name__ == '__main__':

    command = ScoutExportCases(case_id = '643594')

    cases = get_cases_from_scout(command.check_output())

    print(cases)

    command = ScoutExportCases()

    cases = get_cases_from_scout(command.check_output(), days_ago = 100)

    print(cases)
