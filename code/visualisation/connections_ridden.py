# This file is for the plots used in the presentation and not for the experiment
# It uses specific files fromj expqeriment containing 1000 iterations

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

random_summary = pd.read_csv("experiment/random/random_7575/EXPERIMENT_SUMMARY")
greedy_summary = pd.read_csv("experiment/greedy/greedy_2/EXPERIMENT_SUMMARY")

def function_writer_df(algorithm_summary:str,  histogram: bool= False)-> pd.DataFrame:
    """
    Functiom that makes a dataframe for a specific algorithm
    """
    if histogram:
        algorithm = (algorithm_summary.iloc[4][1])
        algorithm_connections = eval(algorithm)
        
        return algorithm_connections

    else:    
        algorithm = (algorithm_summary.iloc[5][1])
        algorithm_connections = eval(algorithm)
        algorithm_df = pd.DataFrame({'Ridden': algorithm_connections})
        
        return algorithm_df

Random = function_writer_df(random_summary)

Greedy = (greedy_summary.iloc[2][1])
greedy_connections = eval(Greedy)

# Create KDE plot using Seaborn
sns.displot(data=Random, x='Ridden', kind='kde', fill=True, label ='Random')
plt.axvline(x=greedy_connections, color='r', alpha=0.5, label='Greedy')

plt.xlabel('Connections ridden')
plt.ylabel('Density')
plt.title('Kernel Density Estimate of connections ridden of 1000 iterations')
plt.legend()

plt.show()