import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#data
iterations = np.arange(1, 11)
Random = [1948.7303370786522, 2465.089887640449, 2220.089887640449, 3070.52808988764, 2786.52808988764, 2651.4494382022467, 1799.2921348314612, 2353.011235955056, 2799.52808988764, 432.4943820224717]
Greedy = [4585.606741573034, 4585.606741573034, 4585.606741573034, 4585.606741573034, 4585.606741573034, 4585.606741573034, 4585.606741573034, 4585.606741573034, 4585.606741573034, 4585.606741573034]
HillClimb = [5489.483146067416, 5485.483146067416, 5434.483146067416, 5490.483146067416, 5465.483146067416, 5597.842696629214, 5490.483146067416, 5485.483146067416, 5492.483146067416, 5482.483146067416]

# Create DataFrame
data = pd.DataFrame({
    "Iterations": iterations,
    "Random": Random,
    "Greedy": Greedy,
    "HillClimb": HillClimb
})

#lineplot
# Transpose the DataFrame to have algorithms as rows and iterations as columns
data_transposed = data.set_index('Iterations').T

# Plot each algorithm's score against iterations
plt.figure(figsize=(10, 6))
for algorithm in data_transposed.index:
    plt.plot(data_transposed.columns, data_transposed.loc[algorithm], marker='o', label=algorithm)

# Customize plot
plt.xlabel('Iterations')
plt.ylabel('Score')
plt.title('Performance of Algorithms over Iterations')
plt.legend(loc='upper left')
plt.grid(True)

# Show plot
plt.show()


# # Create stackplot with transparency
# plt.figure(figsize=(10, 6))
# plt.stackplot(iterations, Random, Greedy, HillClimb, labels=['Random', 'Greedy', 'HillClimb'])

# # Customize plot
# plt.xlabel('Iterations')
# plt.ylabel('Score')
# plt.title('Performance of Algorithms over Iterations')
# plt.legend(loc='upper left')
# plt.grid(True)

# # Show plot
# plt.show()

