import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from .connections_ridden import function_writer_df


random_summary = pd.read_csv("experiment/random/random_7563/EXPERIMENT_SUMMARY")
greedy_summary = pd.read_csv("experiment/greedy/greedy_2/EXPERIMENT_SUMMARY")
# hillclimb_train = pd.read_csv("experiment/hillclimb_train/hillclimb_train_7/EXPERIMENT_SUMMARY")
# hillclimb_connection = pd.read_csv("experiment/hillclimb_connectionslist/hillclimb_train_7/EXPERIMENT_SUMMARY")
# hillclimb_combined = pd.read_csv("experiment/hillclimb_combined/hillclimb_combined_7/EXPERIMENT_SUMMARY")

# The scores for the algorithms
Random = function_writer_df(random_summary, histogram=True)

Greedy = (greedy_summary.iloc[3][1])
greedy_connections = eval(Greedy)

# Hillclimb_connections = (hillclimb_connection.iloc[4][1])
# hill_connections = eval(Hillclimb_connections)

# Hillclimb_trains = (hillclimb_trains.iloc[4][1])
# hill_trains = eval(Hillclimb_trains)

# Hillclimb_combined = (hillclimb_combined.iloc[4][1])
# hill_combined = eval(Hillclimb_combined)

# Plotting histograms
plt.figure(figsize=(10, 6))
plt.hist(Random, bins=100, alpha=0.5, label='Random')
plt.axvline(x=greedy_connections, color='r', alpha=0.5, label='Greedy')

plt.xlabel('Scores')
plt.ylabel('Frequency')
plt.title('Distribution of scores of the algorithms over 1000 Iterations')
plt.legend(loc='upper right')

plt.show()

# # Create a DataFrame from the list
# random_df = pd.DataFrame({'Scores': random_list})

# # Create KDE plot using Seaborn
# sns.displot(data=random_df, x='Scores', kind='kde', fill=True)
# plt.axvline(x=Greedy, color='r', alpha=0.5, label='Greedy')

# plt.xlabel('Scores')
# plt.ylabel('Density')
# plt.title('Kernel Density Estimate of Scores')

# plt.show()