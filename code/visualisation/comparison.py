import csv 
import pandas as pd
# import matplotlib.pyplot as plt



# # Scores for three algorithms
# Random = 
# Greedy = 
# HillClimb_connection = 
# HillClimb_train = 
# HillClimb_combined = 

# # Plotting histograms
# plt.figure(figsize=(10, 6))

# plt.hist(Random, bins=50, alpha=0.5, label='Random')
# plt.hist(Greedy, bins=50, alpha=0.5, label='Greedy')
# plt.hist(HillClimb, bins=50, alpha=0.5, label='HillClimb')

# plt.xlabel('Scores')
# plt.ylabel('Frequency')
# plt.title('Distribution of Scores over Iterations')
# plt.legend(loc='upper right')

# plt.show()
random_data_df = pd.read_csv("experiment/random/random_7562/EXPERIMENT_SUMMARY")
hillclimb_data_df = pd.read_csv("experiment/hillclimb_train/hillclimb_train_7/EXPERIMENT_SUMMARY")

print(random_data_df)

print(hillclimb_data_df)