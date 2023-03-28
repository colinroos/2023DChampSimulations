import pandas as pd
import numpy as np

results = pd.read_csv('outputs/sim_results.csv', index_col=0)

results['mean'] = results.mean(axis=1)

results.sort_values('mean', ascending=False, inplace=True)

rankings = pd.DataFrame(results.index)
rankings.set_index('team', inplace=True)
rankings['pred_rank'] = range(1, len(rankings.index) + 1)
rankings['5th_pct_rank'] = results.drop(['mean'], axis=1).quantile(0.05, axis='rows')
rankings['95th_pct_rank'] = results.drop(['mean'], axis=1).quantile(0.95, axis='rows')

print(results.head(20))
