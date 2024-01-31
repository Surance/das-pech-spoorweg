# das-pech-spoorweg

## The Project

This project focuses on optimizing the rail schedule for trains in the Netherlands. The primary objective is to enhance the efficiency of the intercity train routes, connecting key stations the country. The task is to develop a high quality schedule of train routes that surpasses 89 of the most crucial stations with a maximum of 20 routes, each route not exceeding 180 minutes. 

The optimization function, denoted as K, plays a crucial role in evaluating the quality of the rail route map. The value of K is determined by factors such as the total travel time, the number of critical connections traversed, and the utilization of routes. 

Several algorithms have been developed to maximize the K value, and each algorithm provides a solution in the form of a set of routes tailored to meet the specified criteria for either of the outlined scenarios. 


## Getting Started

To conduct an experiment, you define your requirements within the main function. Additionally, you have the option to specify visualization preferences. In line INPUT LINE, you can choose between matplotlib and plotly visualizations (referred to as visualise_plot and visualise_map, respectively) by setting them to True or False, with the default being True. The advantages of the map/plotly visualisation are that you're able to single out a single traject by double clicking it on the legend. You can also manually remove trains by clicking on them once in the legend. The map visualisation also includes stations that are not written, where you can hover above the stations with your cursor to retrieve the station name. The advantages of the matplotlib/ plot visualisation are that you get to see all the station names in one glance.

### Prerequisites

This code has been fully written in [Python3.9.18](https://www.python.org/downloads/). All neccessary packages to run the code successfully can be found in requirements.txt. These are easy to download using pip dmv. using the following instructions:

```
pip install -r requirements.txt
```

### Structure

The code is structures by the following folders:

- **/code**: contains all code from this project
  - **/code/algorithms**: contains code for the algorithms
  - **/code/classes**: contains the classes needed for the case
  - **/code/visualisation**: contains the code necessary for the visualisation of results
- **/data**: contains the different datafiles needed
- **/experiment**: contains the results from the code, saved per algorithm


### Use

An example can be run by calling the following:

```
python main.py
```

## Authors

* Jimmy Tebben
* Josephine Woltering
* Marieke Gelderloos

## Acknowledgments 

* Minor Artificial Intelligence UvA
* Tim Doolan 
* Wouter Vrielink
* Luka Zaitch
* Jacob Groot