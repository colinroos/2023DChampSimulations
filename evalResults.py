import pandas as pd
import numpy as np

results = pd.read_csv('outputs/sim_results.csv', index_col=0)

results['mean'] = results.mean(axis=1)

results.sort_values('mean', ascending=False, inplace=True)

rankings = pd.DataFrame(results.index)
rankings.set_index('team', inplace=True)

for i in range(1000):
    results.sort_values(str(i), ascending=False, inplace=True)
    rankings = rankings.reindex(results.index)
    rankings[str(i)] = range(1, len(rankings.index) + 1)

# Resort for average case
results.sort_values('mean', ascending=False, inplace=True)
rankings = rankings.reindex(results.index)

summary = pd.DataFrame(rankings.index)
summary.set_index('team', inplace=True)
summary['predicted_rank'] = range(1, len(rankings.index) + 1)
summary.insert(len(summary.columns), 'mean_rank', rankings.mean(axis=1))
summary.insert(len(summary.columns), '5th_percentile', rankings.quantile(0.05, axis=1))
summary.insert(len(summary.columns), '95th_percentile', rankings.quantile(0.95, axis=1))
summary.to_csv('outputs/summary.csv')
rankings.to_csv('outputs/ranking_results.csv')
print(results.head(20))
