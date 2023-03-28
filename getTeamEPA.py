from os.path import exists
import statbotics
import tbapy
import pandas as pd

from privateKeys import TBAkey

# Instantiate API objects
tba = tbapy.TBA(TBAkey)
sb = statbotics.Statbotics()

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

# Load Schedule as generated by Cheezy Arena
sched = pd.read_csv('MatchSchedules/qualification_s1.csv')
sched.set_index('Match', inplace=True)
sched.drop(['Blue1IsSurrogate', 'Blue2IsSurrogate', 'Blue3IsSurrogate', 'Red1IsSurrogate', 'Red2IsSurrogate', 'Red3IsSurrogate'], axis=1, inplace=True)
sched.drop(['Time', 'Type'], axis=1, inplace=True)

# Handle Rankings
ranking = pd.DataFrame(teamsEPA.index)
ranking.set_index('team', inplace=True)
ranking['RP'] = 0
ranking['win'] = 0
ranking['loss'] = 0

# Predict matches
for match in sched.iterrows():
    red1Score = teamsEPA.loc[match[1]['Red1']]['epa_pre_champs']
    red1RP1 = teamsEPA.loc[match[1]['Red1']]['rp_1_epa_pre_champs']
    red1RP2 = teamsEPA.loc[match[1]['Red1']]['rp_2_epa_pre_champs']
    red2Score = teamsEPA.loc[match[1]['Red2']]['epa_pre_champs']
    red2RP1 = teamsEPA.loc[match[1]['Red2']]['rp_1_epa_pre_champs']
    red2RP2 = teamsEPA.loc[match[1]['Red2']]['rp_2_epa_pre_champs']
    red3Score = teamsEPA.loc[match[1]['Red3']]['epa_pre_champs']
    red3RP1 = teamsEPA.loc[match[1]['Red3']]['rp_1_epa_pre_champs']
    red3RP2 = teamsEPA.loc[match[1]['Red3']]['rp_2_epa_pre_champs']
    redScore = red1Score + red2Score + red3Score
    redRP1 = red1RP1 + red2RP1 + red3RP1
    redRP2 = red1RP2 + red2RP2 + red3RP2
    sched.loc[match[0], ['redScore']] = redScore
    blue1Score = teamsEPA.loc[match[1]['Blue1']]['epa_pre_champs']
    blue1RP1 = teamsEPA.loc[match[1]['Blue1']]['rp_1_epa_pre_champs']
    blue1RP2 = teamsEPA.loc[match[1]['Blue1']]['rp_2_epa_pre_champs']
    blue2Score = teamsEPA.loc[match[1]['Blue2']]['epa_pre_champs']
    blue2RP1 = teamsEPA.loc[match[1]['Blue2']]['rp_1_epa_pre_champs']
    blue2RP2 = teamsEPA.loc[match[1]['Blue2']]['rp_2_epa_pre_champs']
    blue3Score = teamsEPA.loc[match[1]['Blue3']]['epa_pre_champs']
    blue3RP1 = teamsEPA.loc[match[1]['Blue3']]['rp_1_epa_pre_champs']
    blue3RP2 = teamsEPA.loc[match[1]['Blue3']]['rp_2_epa_pre_champs']
    blueScore = blue1Score + blue2Score + blue3Score
    blueRP1 = blue1RP1 + blue2RP1 + blue3RP1
    blueRP2 = blue1RP2 + blue2RP2 + blue3RP2
    sched.loc[match[0], ['blueScore']] = blueScore

    redWin = redScore > blueScore
    if redWin:
        redRP = 2 + redRP1 + redRP2
        blueRP = blueRP1 + blueRP2
        ranking.loc[match[1]['Red1'], 'win'] += 1
        ranking.loc[match[1]['Red2'], 'win'] += 1
        ranking.loc[match[1]['Red3'], 'win'] += 1
        ranking.loc[match[1]['Blue1'], 'loss'] += 1
        ranking.loc[match[1]['Blue2'], 'loss'] += 1
        ranking.loc[match[1]['Blue3'], 'loss'] += 1
    else:
        redRP = redRP1 + redRP2
        blueRP = 2 + blueRP1 + blueRP2
        ranking.loc[match[1]['Red1'], 'loss'] += 1
        ranking.loc[match[1]['Red2'], 'loss'] += 1
        ranking.loc[match[1]['Red3'], 'loss'] += 1
        ranking.loc[match[1]['Blue1'], 'win'] += 1
        ranking.loc[match[1]['Blue2'], 'win'] += 1
        ranking.loc[match[1]['Blue3'], 'win'] += 1

    # Store match results
    sched.loc[match[0], 'redWin'] = redWin
    sched.loc[match[0], 'redRP'] = redRP
    sched.loc[match[0], 'blueRP'] = blueRP

    # Store RP
    ranking.loc[match[1]['Red1'], 'RP'] += redRP
    ranking.loc[match[1]['Red2'], 'RP'] += redRP
    ranking.loc[match[1]['Red3'], 'RP'] += redRP

    ranking.loc[match[1]['Blue1'], 'RP'] += blueRP
    ranking.loc[match[1]['Blue2'], 'RP'] += blueRP
    ranking.loc[match[1]['Blue3'], 'RP'] += blueRP

# Save results for later inspection
ranking.sort_values('RP', ascending=False, inplace=True)
ranking.to_csv('outputs/q1_result_rankings.csv')
sched.to_csv('outputs/q1_match_results.csv')
