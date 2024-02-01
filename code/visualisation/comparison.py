# This file is for the plots used in the presentation and not for the experiment
# It uses specific files from experiment containing 1000 iterations

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def function_writer_df(algorithm_summary:str,  histogram: bool= False)-> list or pd.DataFrame:
    """
    Functiom that makes a dataframe for a specific algorithm, histogram has a default setting of false
    """
    # Gives the output for the histogram function
    if histogram:
        algorithm = (algorithm_summary.iloc[4][1])
        algorithm_connections = eval(algorithm)
        
        return algorithm_connections

    # Gives the output for the KDE function
    else:    
        algorithm = (algorithm_summary.iloc[5][1])
        algorithm_connections = eval(algorithm)
        algorithm_df = pd.DataFrame({'Ridden': algorithm_connections})
        
        return algorithm_df


def plot_histogram(random_summary: list, greedy_summary: list, hillclimb_train_summary: list, hillclimb_connection_summary: list, hillclimb_combined_summary: list, bins: int = 100):
    """
    Plot histograms for Random ,Greedy and Hillclimber algorithms.
    """

    # The scores for the algorithms
    Random = function_writer_df(random_summary, histogram=True)
    Hillclimb_train = function_writer_df(hillclimb_train_summary, histogram=True)
    Hillclimb = (hillclimb_connection_summary.iloc[3][1])
    hillclimb_connection= eval(Hillclimb)
    Hillclimb_combined = function_writer_df(hillclimb_combined_summary, histogram=True)
    Greedy = (greedy_summary.iloc[3][1])
    greedy_connections = eval(Greedy)

    # Plotting histograms
    plt.figure(figsize=(10, 6))
   
    plt.hist(Random, bins=bins, alpha=0.5, label='Random')
    plt.hist(Hillclimb_train, color= 'orange', bins=bins, alpha=0.5, label='Hillclimb train')
    plt.hist(Hillclimb_combined, color= 'green', bins=bins, alpha=0.5, label='Hillclimb combined')

    # Plot vertical line for Greedy and Hillclimb connection
    plt.axvline(x=greedy_connections, color='r', linestyle='--', label='Greedy')
    plt.axvline(x=hillclimb_connection, color='purple',linestyle=':', label='Hillclimb connection')

    plt.xlabel('Scores')
    plt.ylabel('Frequency')
    plt.title('Distribution of scores of the algorithms over 1000 Iterations')
    plt.legend(loc='upper right')

    plt.show()


def plot_kde(random_summary: pd.DataFrame, greedy_summary: pd.DataFrame, hillclimb_train_summary: pd.DataFrame, hillclimb_connection_summary: pd.DataFrame, hillclimb_combined_summary: pd.DataFrame):
    """
    Plot Kernel Density Estimate of connections ridden for Random, Greedy and Hillclimber algorithms.
    """

    Random = function_writer_df(random_summary)
    Hillclimb_train = function_writer_df(hillclimb_train_summary)
    Hillclimb_combined = function_writer_df(hillclimb_combined_summary)
    Hillclimb_connection = (hillclimb_connection_summary.iloc[2][1])
    hillclimb_connection= eval(Hillclimb_connection)
    Greedy = (greedy_summary.iloc[2][1])
    greedy_connections = eval(Greedy)

    
    # Create KDE plot using Seaborn
    sns.kdeplot(data=Random, x='Ridden', fill=True, label ='Random')
    sns.kdeplot(data=Hillclimb_train, x='Ridden', fill=True, label='Hillclimb train', alpha=0.5)
    sns.kdeplot(data=Hillclimb_combined, color = 'g', x='Ridden', fill=True, label='Hillclimb combined', alpha=0.2)
  
    # Plot vertical line for Greedy and Hillclimb connection
    plt.axvline(x=greedy_connections, color='r', linestyle='--', label='Greedy')
    plt.axvline(x=hillclimb_connection, color='purple',linestyle=':', label='Hillclimb connection')

    plt.xlabel('Connections ridden')
    plt.ylabel('Density')
    plt.title('Kernel Density Estimate of connections ridden of 1000 iterations')
    plt.legend()
    plt.show()

# Getting the correct files of 1000 iterations
random_summary = pd.read_csv("experiment/random/random_1/EXPERIMENT_SUMMARY")
greedy_summary = pd.read_csv("experiment/greedy/greedy_1/EXPERIMENT_SUMMARY")
hillclimb_train = pd.read_csv("experiment/hillclimb_train/hillclimb_train_1/EXPERIMENT_SUMMARY")
hillclimb_connection = pd.read_csv("experiment/hillclimb_connection/hillclimb_connection_1/EXPERIMENT_SUMMARY")
hillclimb_combined = pd.read_csv("experiment/hillclimb_combined/hillclimb_combined_1/EXPERIMENT_SUMMARY")

# Running both plots
plot_histogram(random_summary, greedy_summary, hillclimb_train, hillclimb_connection, hillclimb_combined)
plot_kde(random_summary, greedy_summary, hillclimb_train, hillclimb_connection, hillclimb_combined)