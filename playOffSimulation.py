import pandas as pd
import numpy as np

from util import *

# Load the team database
teamsEPA = loadTeamEPA()


def play_match(match):
    red1Score = teamsEPA.loc[match['Red1']]['epa_pre_champs']
    red2Score = teamsEPA.loc[match['Red2']]['epa_pre_champs']
    red3Score = teamsEPA.loc[match['Red3']]['epa_pre_champs']
    redScore = red1Score + red2Score + red3Score

    blue1Score = teamsEPA.loc[match['Blue1']]['epa_pre_champs']
    blue2Score = teamsEPA.loc[match['Blue2']]['epa_pre_champs']
    blue3Score = teamsEPA.loc[match['Blue3']]['epa_pre_champs']
    blueScore = blue1Score + blue2Score + blue3Score

    return redScore, blueScore, match


def update_bracket(redScore, blueScore, pmatch, wnext_match, lnext_match, winner_color, loser_color):
    if redScore > blueScore:
        # Red wins
        for j in range(1, 4):
            matches.loc[wnext_match-1, '{}{}'.format(winner_color, j)] = pmatch['Red{}'.format(j)]
        # Blue loses
        if lnext_match > 0:
            for j in range(1, 4):
                matches.loc[lnext_match-1, '{}{}'.format(loser_color, j)] = pmatch['Blue{}'.format(j)]

    else:
        # Blue wins
        for j in range(1, 4):
            matches.loc[wnext_match-1, '{}{}'.format(winner_color, j)] = pmatch['Blue{}'.format(j)]

        if lnext_match > 0:
            # Red loses
            for j in range(1, 4):
                matches.loc[lnext_match-1, '{}{}'.format(loser_color, j)] = pmatch['Red{}'.format(j)]


# Load the simulation results for ranking
pred_rankings = pd.read_csv('outputs/summary.csv')

# Alliance Selection process
alliances = pd.DataFrame(index=range(8), columns=['1pick', '2pick', '3pick'])

# Preload the first place team
alliances.iloc[0]['1pick'] = pred_rankings.iloc[0]['team']
pred_rankings.drop([0], inplace=True)
pred_rankings.reset_index(drop=True, inplace=True)

for i in range(8):
    if alliances.iloc[i]['1pick'] is np.NaN:
        alliances.iloc[i]['1pick'] = pred_rankings.iloc[0]['team']
        pred_rankings.drop([0], inplace=True)
        pred_rankings.reset_index(drop=True, inplace=True)

    if alliances.iloc[i]['2pick'] is np.NaN:
        alliances.iloc[i]['2pick'] = pred_rankings.iloc[0]['team']
        pred_rankings.drop([0], inplace=True)
        pred_rankings.reset_index(drop=True, inplace=True)

for i in range(8):
    if alliances.iloc[7 - i]['3pick'] is np.NaN:
        alliances.iloc[7 - i]['3pick'] = pred_rankings.iloc[0]['team']
        pred_rankings.drop([0], inplace=True)
        pred_rankings.reset_index(drop=True, inplace=True)

print(alliances)

# Build match schedule
matches = pd.DataFrame(index=range(16),
                       columns=['Red1', 'Red2', 'Red3', 'Blue1', 'Blue2', 'Blue3', 'RedScore', 'BlueScore'])
matches.loc[0] = np.concatenate([alliances.iloc[0].values.astype(int), alliances.iloc[7].values.astype(int), np.zeros(2)])
matches.loc[1] = np.concatenate([alliances.iloc[3].values.astype(int), alliances.iloc[4].values.astype(int), np.zeros(2)])
matches.loc[2] = np.concatenate([alliances.iloc[1].values.astype(int), alliances.iloc[6].values.astype(int), np.zeros(2)])
matches.loc[3] = np.concatenate([alliances.iloc[2].values.astype(int), alliances.iloc[5].values.astype(int), np.zeros(2)])

# Play Match 1
rscore, bscore, match = play_match(matches.loc[0])
matches.loc[0]['RedScore'] = rscore
matches.loc[0]['BlueScore'] = bscore
update_bracket(rscore, bscore, match, 7, 5, 'Red', 'Red')

# Play Match 2
rscore, bscore, match = play_match(matches.loc[1])
matches.loc[1]['RedScore'] = rscore
matches.loc[1]['BlueScore'] = bscore
update_bracket(rscore, bscore, match, 7, 5, 'Blue', 'Blue')

# Play Match 3
rscore, bscore, match = play_match(matches.loc[2])
matches.loc[2]['RedScore'] = rscore
matches.loc[2]['BlueScore'] = bscore
update_bracket(rscore, bscore, match, 8, 6, 'Red', 'Red')

# Play Match 4
rscore, bscore, match = play_match(matches.loc[3])
matches.loc[3]['RedScore'] = rscore
matches.loc[3]['BlueScore'] = bscore
update_bracket(rscore, bscore, match, 8, 6, 'Blue', 'Blue')

# Play Match 5
rscore, bscore, match = play_match(matches.loc[4])
matches.loc[4]['RedScore'] = rscore
matches.loc[4]['BlueScore'] = bscore
update_bracket(rscore, bscore, match, 10, -1, 'Blue', 'Red')

# Play Match 6
rscore, bscore, match = play_match(matches.loc[5])
matches.loc[5]['RedScore'] = rscore
matches.loc[5]['BlueScore'] = bscore
update_bracket(rscore, bscore, match, 9, -1, 'Blue', 'Red')

# Play Match 7
rscore, bscore, match = play_match(matches.loc[6])
matches.loc[6]['RedScore'] = rscore
matches.loc[6]['BlueScore'] = bscore
update_bracket(rscore, bscore, match, 11, 9, 'Red', 'Red')

# Play Match 8
rscore, bscore, match = play_match(matches.loc[7])
matches.loc[7]['RedScore'] = rscore
matches.loc[7]['BlueScore'] = bscore
update_bracket(rscore, bscore, match, 11, 10, 'Blue', 'Red')

# Play Match 9
rscore, bscore, match = play_match(matches.loc[8])
matches.loc[8]['RedScore'] = rscore
matches.loc[8]['BlueScore'] = bscore
update_bracket(rscore, bscore, match, 12, -1, 'Blue', 'Red')

# Play Match 10
rscore, bscore, match = play_match(matches.loc[9])
matches.loc[9]['RedScore'] = rscore
matches.loc[9]['BlueScore'] = bscore
update_bracket(rscore, bscore, match, 12, -1, 'Red', 'Red')

# Play Match 11
rscore, bscore, match = play_match(matches.loc[10])
matches.loc[10]['RedScore'] = rscore
matches.loc[10]['BlueScore'] = bscore
update_bracket(rscore, bscore, match, 14, 13, 'Red', 'Red')

# Play Match 12
rscore, bscore, match = play_match(matches.loc[11])
matches.loc[11]['RedScore'] = rscore
matches.loc[11]['BlueScore'] = bscore
update_bracket(rscore, bscore, match, 13, -1, 'Blue', 'Red')

# Play Match 13
rscore, bscore, match = play_match(matches.loc[12])
matches.loc[12]['RedScore'] = rscore
matches.loc[12]['BlueScore'] = bscore
update_bracket(rscore, bscore, match, 14, -1, 'Blue', 'Red')

# Play Match 14
rscore, bscore, match = play_match(matches.loc[13])
matches.loc[13]['RedScore'] = rscore
matches.loc[13]['BlueScore'] = bscore
update_bracket(rscore, bscore, match, 15, -1, 'Red', 'Blue')

print(0)
