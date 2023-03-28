from util import *
from scheduler import *
import pandas as pd
from glob import glob


class CompetitionSimulator:
    sched = pd.DataFrame()
    teamsEPA = pd.DataFrame()
    ranking = pd.DataFrame()
    sim_results = pd.DataFrame()
    num_simulations = 100

    def __init__(self):
        self.teamsEPA = loadTeamEPA()

        # generate schedules
        if len(glob('db/*_match_schedule.pkl')) < self.num_simulations:
            buildRandomSchedule(self.teamsEPA.index, self.num_simulations)

        # Load schedules
        self.loadSched(0)

        self.sim_results = pd.DataFrame(self.teamsEPA.index)
        self.sim_results.set_index('team', inplace=True)

    def loadSched(self, index):
        # Load schedules
        self.sched = loadSchedule(index)

        # Handle Rankings
        self.ranking = pd.DataFrame(self.teamsEPA.index)
        self.ranking.set_index('team', inplace=True)
        self.ranking['RP'] = 0
        self.ranking['win'] = 0
        self.ranking['loss'] = 0

    def simulate(self):

        for sim in range(self.num_simulations):

            print('Simulating iteration {}'.format(sim))
            self.loadSched(sim)

            for match in self.sched.iterrows():
                red1Score = self.teamsEPA.loc[match[1]['Red1']]['epa_pre_champs']
                red1RP1 = self.teamsEPA.loc[match[1]['Red1']]['rp_1_epa_pre_champs']
                red1RP2 = self.teamsEPA.loc[match[1]['Red1']]['rp_2_epa_pre_champs']
                red2Score = self.teamsEPA.loc[match[1]['Red2']]['epa_pre_champs']
                red2RP1 = self.teamsEPA.loc[match[1]['Red2']]['rp_1_epa_pre_champs']
                red2RP2 = self.teamsEPA.loc[match[1]['Red2']]['rp_2_epa_pre_champs']
                red3Score = self.teamsEPA.loc[match[1]['Red3']]['epa_pre_champs']
                red3RP1 = self.teamsEPA.loc[match[1]['Red3']]['rp_1_epa_pre_champs']
                red3RP2 = self.teamsEPA.loc[match[1]['Red3']]['rp_2_epa_pre_champs']
                redScore = red1Score + red2Score + red3Score
                redRP1 = red1RP1 + red2RP1 + red3RP1
                redRP2 = red1RP2 + red2RP2 + red3RP2
                self.sched.loc[match[0], ['redScore']] = redScore
                blue1Score = self.teamsEPA.loc[match[1]['Blue1']]['epa_pre_champs']
                blue1RP1 = self.teamsEPA.loc[match[1]['Blue1']]['rp_1_epa_pre_champs']
                blue1RP2 = self.teamsEPA.loc[match[1]['Blue1']]['rp_2_epa_pre_champs']
                blue2Score = self.teamsEPA.loc[match[1]['Blue2']]['epa_pre_champs']
                blue2RP1 = self.teamsEPA.loc[match[1]['Blue2']]['rp_1_epa_pre_champs']
                blue2RP2 = self.teamsEPA.loc[match[1]['Blue2']]['rp_2_epa_pre_champs']
                blue3Score = self.teamsEPA.loc[match[1]['Blue3']]['epa_pre_champs']
                blue3RP1 = self.teamsEPA.loc[match[1]['Blue3']]['rp_1_epa_pre_champs']
                blue3RP2 = self.teamsEPA.loc[match[1]['Blue3']]['rp_2_epa_pre_champs']
                blueScore = blue1Score + blue2Score + blue3Score
                blueRP1 = blue1RP1 + blue2RP1 + blue3RP1
                blueRP2 = blue1RP2 + blue2RP2 + blue3RP2
                self.sched.loc[match[0], ['blueScore']] = blueScore

                redWin = redScore > blueScore
                if redWin:
                    redRP = 2 + redRP1 + redRP2
                    blueRP = blueRP1 + blueRP2
                    self.ranking.loc[match[1]['Red1'], 'win'] += 1
                    self.ranking.loc[match[1]['Red2'], 'win'] += 1
                    self.ranking.loc[match[1]['Red3'], 'win'] += 1
                    self.ranking.loc[match[1]['Blue1'], 'loss'] += 1
                    self.ranking.loc[match[1]['Blue2'], 'loss'] += 1
                    self.ranking.loc[match[1]['Blue3'], 'loss'] += 1
                else:
                    redRP = redRP1 + redRP2
                    blueRP = 2 + blueRP1 + blueRP2
                    self.ranking.loc[match[1]['Red1'], 'loss'] += 1
                    self.ranking.loc[match[1]['Red2'], 'loss'] += 1
                    self.ranking.loc[match[1]['Red3'], 'loss'] += 1
                    self.ranking.loc[match[1]['Blue1'], 'win'] += 1
                    self.ranking.loc[match[1]['Blue2'], 'win'] += 1
                    self.ranking.loc[match[1]['Blue3'], 'win'] += 1

                # Store match results
                self.sched.loc[match[0], 'redWin'] = redWin
                self.sched.loc[match[0], 'redRP'] = redRP
                self.sched.loc[match[0], 'blueRP'] = blueRP

                # Store RP
                self.ranking.loc[match[1]['Red1'], 'RP'] += redRP
                self.ranking.loc[match[1]['Red2'], 'RP'] += redRP
                self.ranking.loc[match[1]['Red3'], 'RP'] += redRP

                self.ranking.loc[match[1]['Blue1'], 'RP'] += blueRP
                self.ranking.loc[match[1]['Blue2'], 'RP'] += blueRP
                self.ranking.loc[match[1]['Blue3'], 'RP'] += blueRP

            # Save simulation results to dataframe
            self.sim_results[sim] = self.ranking['RP']

        self.sim_results.to_csv('outputs/sim_results.csv')


if __name__ == '__main__':
    sim = CompetitionSimulator()
    sim.simulate()
