import csv 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

random_summary = pd.read_csv("experiment/random/random_7563/EXPERIMENT_SUMMARY")

Random = (random_summary.iloc[4]['random'])
random_list = eval(Random)
Greedy = [4914.483146067416] 

# Plotting histograms
plt.figure(figsize=(10, 6))
plt.hist(random_list, bins=100, alpha=0.5, label='Random')
plt.axvline(x=Greedy, color='r', alpha=0.5, label='Greedy')

plt.xlabel('Scores')
plt.ylabel('Frequency')
plt.title('Distribution of scores of the algorithms over 1000 Iterations')
plt.legend(loc='upper right')

plt.show()

# # Create a DataFrame from the list
# random_df = pd.DataFrame({'Scores': Random})

# # Create KDE plot using Seaborn
# sns.displot(data=random_df, x='Scores', kind='kde', fill=True)

# plt.xlabel('Scores')
# plt.ylabel('Density')
# plt.title('Kernel Density Estimate of Scores')

# plt.show()

# # Scores for three algorithms
# Random = 
# Greedy = 
# HillClimb_connection = 
# HillClimb_train = 
# HillClimb_combined = 


# plt.hist(Greedy, bins=50, alpha=0.5, label='Greedy')
# plt.hist(HillClimb, bins=50, alpha=0.5, label='HillClimb')


# random_data_df = pd.read_csv("experiment/random/random_7563/EXPERIMENT_SUMMARY")
# hillclimb_data_df = pd.read_csv("experiment/hillclimb_train/hillclimb_train_7/EXPERIMENT_SUMMARY")

# print(random_data_df)

# print(hillclimb_data_df)