import math

import numpy as np
import pandas as pd


def buildRandomSchedule(teams, numschedules):
    print('Generating {} match schedules'.format(numschedules))
    numTeams = len(teams)
    matchesPerTeam = 12
    TeamsPerMatch = 6
    num_matches = int(math.ceil(float(numTeams) * float(matchesPerTeam) / TeamsPerMatch))

    csvLines = np.loadtxt('Schedules/' + str(numTeams) + '_' + str(matchesPerTeam) + '.csv', delimiter=',')

    anonSchedule = np.zeros((num_matches, 12))

    teams = np.array(teams)

    for i in range(num_matches):
        for j in range(12):
            anonSchedule[i, j] = csvLines[i, j]

    for i in range(numschedules):
        print('Generating schedule {}'.format(i+1))
        matches = pd.DataFrame(columns=['Red1', 'Red1IsSurrogate', 'Red2', 'Red2IsSurrogate', 'Red3', 'Red3IsSurrogate',
                                        'Blue1', 'Blue1IsSurrogate', 'Blue2', 'Blue2IsSurrogate', 'Blue3',
                                        'Blue3IsSurrogate'])

        np.random.shuffle(teams)

        for idx, anonMatch in enumerate(anonSchedule):
            matches.loc[idx, 'Red1'] = teams[int(anonMatch[0] - 1)]
            matches.loc[idx, 'Red2'] = teams[int(anonMatch[2] - 1)]
            matches.loc[idx, 'Red3'] = teams[int(anonMatch[4] - 1)]
            matches.loc[idx, 'Blue1'] = teams[int(anonMatch[6] - 1)]
            matches.loc[idx, 'Blue2'] = teams[int(anonMatch[8] - 1)]
            matches.loc[idx, 'Blue3'] = teams[int(anonMatch[10] - 1)]

        filepath = 'db/' + str(i) + '_match_schedule.pkl'
        matches.to_pickle(filepath)
