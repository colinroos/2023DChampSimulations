from os.path import exists
import statbotics
import tbapy
import pandas as pd

from privateKeys import TBAkey

# Instantiate API objects
tba = tbapy.TBA(TBAkey)
sb = statbotics.Statbotics()


def loadTeamEPA():
    if exists('db/teamsEPA.csv'):
        teamsEPA = pd.read_csv('db/teamsEPA.csv', index_col=0)
    else:
        # Load Team list, limit to top 80 (for district champs)
        dTeams = tba.district_rankings('2023ont')[:80]
        teams = []
        for team in dTeams:
            team_num = int(team.team_key[3:])
            team_stats = sb.get_team_year(team_num, 2023)
            teams.append(team_stats)

        # Create a dataframe from the fetched EPA values for each team, save to local DB
        teamsEPA = pd.DataFrame(teams)
        teamsEPA.set_index('team', inplace=True)
        teamsEPA.to_csv('db/teamsEPA.csv')

    return teamsEPA


def loadSchedule(index):
    # Load Schedule as generated by Cheezy Arena
    sched = pd.read_pickle('db/{}_match_schedule.pkl'.format(index))
    sched.drop(['Blue1IsSurrogate', 'Blue2IsSurrogate', 'Blue3IsSurrogate', 'Red1IsSurrogate', 'Red2IsSurrogate',
                'Red3IsSurrogate'], axis=1, inplace=True)
    # sched.drop(['Time', 'Type'], axis=1, inplace=True)
    return sched